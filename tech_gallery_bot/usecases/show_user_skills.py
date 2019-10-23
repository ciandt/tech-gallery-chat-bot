from tech_gallery_bot.domain import UserProfile


class ShowUserSkills:
    def __init__(self, user_repository, user_profile_repository):
        self._user_repository = user_repository
        self._user_profile_repository = user_profile_repository

    def execute(self, email, limit):
        user = self._user_repository.find_by_email(email)
        if user is None:
            return None

        profile = self._user_profile_repository.find_by_user(user)
        if profile is None:
            return None

        profile.technologies.sort(key=lambda k: (k.skill, k.endorsements), reverse=True)

        technologies = list(filter(lambda x: x.skill > 0, profile.technologies))

        if len(technologies) > limit:
            technologies = technologies[:limit]

        return ShowUserSkillsResult(user=user, technologies=technologies)


class ShowUserSkillsResult(UserProfile):
    pass
