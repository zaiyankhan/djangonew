from cms.api import get_page_draft
from cms.extensions.toolbar import ExtensionToolbar
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.utils.page_permissions import user_can_change_page
from django.core.urlresolvers import reverse, NoReverseMatch
from website.models.cms_extension import HeaderBackgroundExtension, HighlightedMenuExtension


@toolbar_pool.register
class HeaderBackgroundExtensionToolbar(CMSToolbar):
    def populate(self):
        # always use draft if we have a page
        self.page = get_page_draft(self.request.current_page)

        if not self.page:
            # Nothing to do
            return

        if user_can_change_page(user=self.request.user, page=self.page):
            try:
                icon_extension = HeaderBackgroundExtension.objects.get(extended_object_id=self.page.id)
            except HeaderBackgroundExtension.DoesNotExist:
                icon_extension = None
            try:
                if icon_extension:
                    url = reverse('admin:website_headerbackgroundextension_change', args=(icon_extension.pk,))
                else:
                    url = reverse('admin:website_headerbackgroundextension_add') + '?extended_object=%s' % self.page.pk
            except NoReverseMatch:
                pass
            else:
                not_edit_mode = not self.toolbar.edit_mode
                current_page_menu = self.toolbar.get_or_create_menu('page')
                current_page_menu.add_modal_item("Page background", url=url, disabled=not_edit_mode)


@toolbar_pool.register
class HighlightedMenuExtensionToolbar(ExtensionToolbar):
    # defines the model for the current toolbar
    model = HighlightedMenuExtension

    def populate(self):
        # setup the extension toolbar with permissions and sanity checks
        current_page_menu = self._setup_extension_toolbar()

        # if it's all ok
        if current_page_menu:
            # retrieves the instance of the current extension (if any) and the toolbar item URL
            page_extension, url = self.get_page_extension_admin()
            if url:
                # adds a toolbar item in position 0 (at the top of the menu)
                current_page_menu.add_modal_item('Link color', url=url,
                                                 disabled=not self.toolbar.edit_mode, position=0)