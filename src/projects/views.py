from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from projects.models.projects import Project
from projects.models.participants_in_project import ParticipantInProject
from projects.serializers.projects import ProjectsSerializer


class ProjectViewSet(GenericViewSet, mixins.ListModelMixin):
    """
    A viewset for listing project instances.

    Provides the following action:
    - `list`: Retrieve a list of all projects.

    Attributes:
    - `queryset`: A queryset for retrieving project instances.
    - `serializer_class`: The serializer class used for validating and serializing data.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer


class ProjectsOverviewView(APIView):
    """
    Return dynamic json with a list of projects
    """

    def query_to_json(self, query):
        """
        Convert a queryset of projects into a json serializable format.

        Args:
            query: A queryset of Project instances.

        Returns:
            A list of dictionaries representing project details.
        """
        result = []

        for project in query:
            needed_participants = sum(
                role.participants_needed for role in project.rolesinproject_set.all()
            )
            amount_particpants = ParticipantInProject.objects.filter(
                project=project
            ).count()
            free_slots = needed_participants - amount_particpants

            res = {
                "id": project.pk,
                "name": project.project_name,
                "status": project.status,
                "participants_needed": needed_participants,
                "free_slots": free_slots if free_slots >= 0 else 0,
                "finished_at": project.finish_date,
                "technologies": [tool.tool_name for tool in project.tools.all()],
            }
            result.append(res)

        return result

    def filter_unique_dates(self, query):
        """
        Filter projects to ensure each project has a unique finish date.

        Args:
            query: A queryset of Project instances.

        Returns:
            A list of projects with unique finish dates.
        """
        unique_projects = []
        unique_dates = set()

        for project in query:
            if project.finish_date not in unique_dates:
                unique_dates.add(project.finish_date)
                unique_projects.append(project)

        return unique_projects

    def filter_unique_tools(self, query):
        """
        Filter projects to ensure each project has a unique set of tools.

        Args:
            query: A queryset of Project instances.

        Returns:
            A list of projects with unique tools.
        """
        unique_projects = []
        unique_tools = set()

        for project in query:
            if project.tools not in unique_tools:
                unique_tools.add(project.finish_date)
                unique_projects.append(project)

        return unique_projects

    def filter_participants_amount(self, query):
        """
        Filter projects so theres no more than 3 projects with the same amount.


        Args:
            query: A queryset of Project instances.

        Returns:
            A list of projects with a unique number of participants (max 3 for each count).
        """
        unique_projects = []
        participants_count = {}

        for project in query:
            participants_needed = sum(
                role.participants_needed for role in project.rolesinproject_set.all()
            )

            if participants_count.get(participants_needed, 0) < 3:
                unique_projects.append(project)
                participants_count[participants_needed] = (
                    participants_count.get(participants_needed, 0) + 1
                )

        return unique_projects

    def filter_free_slots(self, query):
        """
        Filter projects to include only those with available participant slots.

        Args:
            query: A queryset of Project instances.

        Returns:
            A list of projects with free slots for participants.
        """
        free_slots_projects = []

        for project in query:
            needed_participants = sum(
                role.participants_needed for role in project.rolesinproject_set.all()
            )
            amount_particpants = ParticipantInProject.objects.filter(
                project=project
            ).count()
            free_slots = needed_participants - amount_particpants
            if free_slots > 0:
                free_slots_projects.append(project)

        return free_slots_projects

    def get(self, request):
        """
        Handle GET requests to retrieve projects for the front page.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object containing project data in JSON format.
        """
        unfinished_projects = Project.objects.filter(status="NF").order_by(
            "finish_date"
        )[:8]
        finished_projects = Project.objects.filter(status="FN").order_by(
            "-finish_date"
        )[:8]

        # Apply various filters to ensure uniqueness and validity of projects
        unfinished_projects = self.filter_unique_dates(unfinished_projects)
        finished_projects = self.filter_unique_dates(finished_projects)

        unfinished_projects = self.filter_unique_tools(unfinished_projects)
        finished_projects = self.filter_unique_tools(finished_projects)

        unfinished_projects = self.filter_participants_amount(unfinished_projects)
        finished_projects = self.filter_participants_amount(finished_projects)

        unfinished_projects = self.filter_free_slots(unfinished_projects)

        res = self.query_to_json(unfinished_projects) + self.query_to_json(
            finished_projects
        )
        return Response({"projects": res[:6]}, status=status.HTTP_200_OK)
