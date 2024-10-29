# Here are functions that create test instances of specific application models

from accounts.models.custom_user import CustomUser
from common.models.roles import Role
from common.models.tags import Tag
from common.models.tools import Tool
from hackathons.models.groups_for_hackathons import GroupsForHackathon
from hackathons.models.groups_in_hackathon import GroupsInHackathon
from hackathons.models.hackathon_participation_request import (
    HackathonParticipationRequest,
)
from hackathons.models.hackathon_prizes import HackathonPrizes
from hackathons.models.hackathons import Hackathon
from hackathons.models.participant_in_hackathon_groups import (
    ParticipantInHackathonGroups,
)
from hackathons.models.participant_in_hackathon_roles import ParticipantInHackathonRoles
from hackathons.models.participant_in_hackathon_tools import ParticipantInHackathonTools
from hackathons.models.participants_in_hackathon import ParticipantsInHackathon
from profiles.models.profiles import Profile
from projects.models.groups_for_projects import Group
from projects.models.project_types import ProjectType
from projects.models.projects import Project
from projects.models.roles_in_project import RolesInProject
from projects.models.tools_in_project import ToolsInProject


def create_instance_common():
    pass


def create_instance_hackathons():

    hackathon = Hackathon.objects.create(
        name="Hackathons New",
        core_idea="Core idea",
        task="lorem task",
        image_url="lorem",
    )

    hackathonsprize = HackathonPrizes.objects.create(
        prize=hackathon,
        name="Example Hackathons Prizes",
        description="Example Hackathons Prizes Description",
    )

    groupinhackathon = GroupsInHackathon.objects.create(hackathon=hackathon)
    groupforhackathon = GroupsForHackathon.objects.create(
        group=groupinhackathon, group_name="Example Group for Hackathons"
    )

    participantinhackathon = ParticipantsInHackathon.objects.create(
        hackathon=hackathon,
    )

    participantinhackathongroup = ParticipantInHackathonGroups.objects.create(
        participant=participantinhackathon, group=groupforhackathon
    )

    role = Role.objects.create(role_name="Participants")

    participantinhackathonrole = ParticipantInHackathonRoles.objects.create(
        participant=participantinhackathon, role=role
    )

    tool = Tool.objects.create(tool_name="Git")

    participantinhackathontool = ParticipantInHackathonTools.objects.create(
        participant=participantinhackathon, tool=tool
    )

    user = CustomUser.objects.create_user(
        username="existinguser1",
        email="existinguser1@example.com",
        password="Testpassword123",
    )
    profile = Profile.objects.create(user=user)

    participantinhackathonrequest = HackathonParticipationRequest.objects.create(
        profile=profile, hackathon=hackathon
    )


def create_instance_profiles():
    pass


def create_instance_projects():
    # Создание типов проектов
    type1 = ProjectType.objects.create(type_name="Backend")

    # Создание ролей
    role1 = Role.objects.create(role_name="Developer")
    role2 = Role.objects.create(role_name="Designer")

    # Создание групп
    group1 = Group.objects.create(group_name="Group A")

    # Создание инструментов
    tool1 = Tool.objects.create(tool_name="Git")
    tool2 = Tool.objects.create(tool_name="Docker")

    # Создание тегов
    tag1 = Tag.objects.create(tag_name="Python")
    tag2 = Tag.objects.create(tag_name="Django")

    # Создание проекта
    project1 = Project.objects.create(
        project_type=type1,
        project_name="Project 1",
        core_idea="Core idea of project 1",
        description="Description of project 1",
        finish_date="2024-12-31",
        status=Project.ProjectStatus.NOT_STARTED,
    )

    # Добавление информации о количестве участников для каждой роли и инструмента
    RolesInProject.objects.create(role=role1, project=project1, participants_needed=4)
    RolesInProject.objects.create(role=role2, project=project1, participants_needed=5)
    ToolsInProject.objects.create(tool=tool1, project=project1, participants_needed=6)
    ToolsInProject.objects.create(tool=tool2, project=project1, participants_needed=7)

    # Добавление связей ManyToMany
    project1.tags.set([tag1, tag2])
    project1.groups.set([group1])
