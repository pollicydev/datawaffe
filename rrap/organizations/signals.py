from wagtail.core.signals import page_published
from django.contrib.auth.models import Permission
from wagtail.core.models import (
    Group,
    Collection,
    GroupCollectionPermission,
    GroupPagePermission,
    Page,
)
from .models import OrganisationPage

# create a group and collection for that organisation
def organisation_created_receiver(sender, instance, **kwargs):

    admin_permission = Permission.objects.get(
        content_type__app_label="wagtailadmin", codename="access_admin"
    )
    # create collection
    try:
        new_collection = Collection.objects.get(name=instance.title)
    except Collection.DoesNotExist:
        try:
            root_collection = Collection.get_first_root_node()
            new_collection = root_collection.add_child(name=instance.title)
            new_group = Group.objects.create(name=instance.title)
            # group users can access cms
            new_group.permissions.add(admin_permission)
            # give group permission to organisation page
            new_page = Page.objects.get(id=instance.id)
            GroupPagePermission.objects.create(
                group=new_group, page=new_page, permission_type="edit"
            )
            GroupPagePermission.objects.create(
                group=new_group, page=new_page, permission_type="publish"
            )

            # give group permission to named collection (and by extension images and docs)
            GroupCollectionPermission.objects.create(
                group=new_group,
                collection=new_collection,
                permission=Permission.objects.get(
                    content_type__app_label="wagtailimages", codename="add_image"
                ),
            )
            GroupCollectionPermission.objects.create(
                group=new_group,
                collection=new_collection,
                permission=Permission.objects.get(
                    content_type__app_label="wagtailimages", codename="change_image"
                ),
            )
            GroupCollectionPermission.objects.create(
                group=new_group,
                collection=new_collection,
                permission=Permission.objects.get(
                    content_type__app_label="wagtailimages", codename="choose_image"
                ),
            )

            GroupCollectionPermission.objects.create(
                group=new_group,
                collection=new_collection,
                permission=Permission.objects.get(
                    content_type__app_label="wagtaildocs", codename="add_document"
                ),
            )
            GroupCollectionPermission.objects.create(
                group=new_group,
                collection=new_collection,
                permission=Permission.objects.get(
                    content_type__app_label="wagtaildocs", codename="change_document"
                ),
            )
            GroupCollectionPermission.objects.create(
                group=new_group,
                collection=new_collection,
                permission=Permission.objects.get(
                    content_type__app_label="wagtaildocs", codename="choose_document"
                ),
            )

        except Exception:
            raise


page_published.connect(organisation_created_receiver, sender=OrganisationPage)
