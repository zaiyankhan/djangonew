from cms.models import Page
from django.urls import reverse
from menus.base import NavigationNode, Modifier
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _
from cms.menu_bases import CMSAttachMenu


class UserMenu(CMSAttachMenu):
    name = "User menu"

    def get_nodes(self, request):
        return [
            NavigationNode(_("Profile"), reverse("user-profile"), 1, attr={'visible_for_anonymous': False}),
            NavigationNode(_("Sign in"), reverse("account_login"), 3, attr={'visible_for_authenticated': False}),
            NavigationNode(_("Sign up"), reverse("account_signup"), 4, attr={'visible_for_authenticated': False}),
            NavigationNode(_("Log out"), reverse("account_logout"), 2, attr={'visible_for_anonymous': False}),
        ]


menu_pool.register_menu(UserMenu)


class MainMenuModifier(Modifier):
    """
    This modifier makes the changed_by attribute of a page
    accessible for the menu system.
    """

    def modify(self, request, nodes, namespace, root_id, post_cut, breadcrumb):
        # only do something when the menu has already been cut
        if post_cut:
            # only consider nodes that refer to cms pages
            # and put them in a dict for efficient access
            page_nodes = {n.id: n for n in nodes if 'is_page' in n.attr and n.attr["is_page"]}
            # retrieve the attributes of interest from the relevant pages
            pages = Page.objects.filter(id__in=page_nodes.keys())
            # loop over all relevant pages
            for page in pages:
                try:
                    highlighted = page.highlightedmenuextension
                    color = highlighted.color
                    background_color = highlighted.button_background_color
                    button_like = highlighted.button_like
                    node = page_nodes[page.pk]
                    if color:
                        node.attr["color"] = color
                    if button_like:
                        node.attr["button_like"] = button_like
                    if background_color:
                        node.attr["background_color"] = background_color
                except Exception as e:
                    pass
        return nodes


menu_pool.register_modifier(MainMenuModifier)