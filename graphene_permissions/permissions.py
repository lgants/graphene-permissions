from typing import Any

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
    app_lab = ''
    model_name = ''
    perms_map = {
        'add': [f'{app_lab}.add_{model_name}'],
        'change': [f'{app_lab}.change_{model_name}'],
        'delete': [f'{app_lab}.delete_{model_name}'],
    }

    def has_node_permission(self, info: ResolveInfo, id: str) -> bool:
        return True

    def has_mutation_permission(self, root: Any, info: ResolveInfo, input: dict) -> bool:
        return info.context.user.has_perms(self.perms_map['add'])

    def has_filter_permission(self, info: ResolveInfo) -> bool:
        return True
