from typing import Any, Union

from graphql import ResolveInfo


class AllowAny:
    """
    Basic authentication class.
    Allows any user for any action.
    Subclass it and override methods below.
    """

    @staticmethod
    def has_node_permission(info: ResolveInfo, id: str) -> bool:
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    @staticmethod
    def has_mutation_permission(root: Any, info: ResolveInfo, input: dict) -> bool:
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    @staticmethod
    def has_filter_permission(info: ResolveInfo) -> bool:
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class AllowAuthenticated:
    """
    Allows performing action only for logged in users.
    """

    @staticmethod
    def has_node_permission(info: ResolveInfo, id: str) -> bool:
        return info.context.user.is_authenticated

    @staticmethod
    def has_mutation_permission(root: Any, info: ResolveInfo, input: dict) -> bool:
        return info.context.user.is_authenticated

    @staticmethod
    def has_filter_permission(info: ResolveInfo) -> bool:
        return info.context.user.is_authenticated


class AllowStaff:
    """
    Allow performing action only for staff users.
    """

    @staticmethod
    def has_node_permission(info: ResolveInfo, id: str) -> bool:
        return info.context.user.is_staff

    @staticmethod
    def has_mutation_permission(root: Any, info: ResolveInfo, input: dict) -> bool:
        return info.context.user.is_staff

    @staticmethod
    def has_filter_permission(info: ResolveInfo) -> bool:
        return info.context.user.is_staff


class AllowSuperuser:
    """
    Allow performing action only for superusers.
    """

    @staticmethod
    def has_node_permission(info: ResolveInfo, id: str) -> bool:
        return info.context.user.is_superuser

    @staticmethod
    def has_mutation_permission(root: Any, info: ResolveInfo, input: dict) -> bool:
        return info.context.user.is_superuser

    @staticmethod
    def has_filter_permission(info: ResolveInfo) -> bool:
        return info.context.user.is_superuser


class DjangoModelPermission:
    app_label: str = ''
    model_name: str = ''
    perms_map: dict = {
        'add': [f'{app_label}.add_{model_name}'],
        'change': [f'{app_label}.change_{model_name}'],
        'delete': [f'{app_label}.delete_{model_name}'],
    }

    def resolve_permission(self, user: 'get_user_model', permissions: Union[list, tuple]) -> bool:
        return all([user.has_perm(self.perms_map[i]) for i in permissions])

    def has_node_permission(self, info: ResolveInfo, id: str) -> bool:
        return True

    def has_mutation_permission(self, root: Any, info: ResolveInfo, input: dict) -> bool:
        return self.resolve_permission(info.context.user, ('add', 'change', 'delete'))

    def has_filter_permission(self, info: ResolveInfo) -> bool:
        return True
