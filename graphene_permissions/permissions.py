from typing import Any, Union, Dict, List

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
    """
    Map django model permissions to .
    """
    # def _get_app_label(self):
    #     return self.app_label

    # def _get_model_name(self):
        # return self.model_name

    app_label: str = ''
    model_name: str = ''
    perms_map: Dict[str, List[str]] = {
        'read': [],
        'add': ['{}.add_{}'],
        'change': ['{}.change_{}'],
        'delete': ['{}.delete_{}'],
    }

    def get_perms(self, methods):
        methods = ['add',]
        kwargs = {
            'app_label': self.app_label,
            'model_name': self.model_name,
        }


        return [j.format(**kwargs) for j in self.perms_map[j] for j in methods]
        # pass

    def _resolve_permission(self, user: 'get_user_model', permissions: Union[list, tuple]) -> bool:
        return all([user.has_perms(self.perms_map[i]) for i in permissions])

    def has_node_permission(self, info: ResolveInfo, id: str) -> bool:
        return self._resolve_permission(info.context.user, ['read'])

    def has_mutation_permission(self, root: Any, info: ResolveInfo, input: dict) -> bool:
        print (self.get_perms(['add']))
        return self._resolve_permission(info.context.user, ['add'])

    def has_filter_permission(self, info: ResolveInfo) -> bool:
        return self._resolve_permission(info.context.user, ['read'])
