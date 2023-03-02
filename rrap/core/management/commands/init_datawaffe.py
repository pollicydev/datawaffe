from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from wagtail.core.models import Page, Site
from wagtailmenus.models import MainMenuItem, MainMenu, FlatMenu, FlatMenuItem

from rrap.blog.models import BlogIndexPage
from rrap.organizations.models import OrganisationIndexPage
from rrap.core.models import HomePage, StandardPage, PublicationsIndexPage, ContactPage

User = get_user_model()


def create_superuser(name, email, password):
    try:
        return User.objects.create_superuser(name, email, password)
    except:
        pass


class Command(BaseCommand):
    @atomic
    def handle(self, *args, **options):
        print("  Creating Pages... ", end="", flush=True)
        ### clear page tree
        Page.objects.first().get_root().get_children().delete()

        root_page = Page.objects.get(path="0001")
        home_page = HomePage(title="Data Waffe", slug="home")
        root_page.add_child(instance=home_page)
        home_page.save()

        site, _ = Site.objects.get_or_create(
            hostname="datawaffe.org",
            root_page=home_page,
            is_default_site=True,
        )

        orgs_index = OrganisationIndexPage(
            title="Organisations", slug="organisations", show_in_menus=True
        )
        home_page.add_child(instance=orgs_index)

        pubs_index = PublicationsIndexPage(
            title="Publications", slug="publications", show_in_menus=True
        )
        home_page.add_child(instance=pubs_index)

        blog_index = BlogIndexPage(
            title="Blog",
            seo_title="News & Commentary",
            introduction="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            show_in_menus=True,
        )
        home_page.add_child(instance=blog_index)

        contact_page = ContactPage(
            title="Contact us",
            slug="contact",
            show_in_menus=True,
            to_address="info@pollicy.org",
            from_address="website@datawaffe.org",
            subject="Data Waffe Contact Form Request",
            intro='<p data-block-key="jp01j">Get in touch with us by filling out this form.</p>',
            thank_you_text='<p data-block-key="muh8m">Thank you for reaching out. A representative will be in touch with you soon, if necessary.</p>',
        )
        # no form fields object setup so has to be manual
        home_page.add_child(instance=contact_page)

        # Standard pages
        about_page = StandardPage(title="About", body="", show_in_menus=True)
        home_page.add_child(instance=about_page)
        toc_page = StandardPage(
            title="Terms and Conditions", body="", show_in_menus=True
        )
        home_page.add_child(instance=toc_page)
        privacy_policy_page = StandardPage(
            title="Privacy Policy", body="", show_in_menus=True
        )
        home_page.add_child(instance=privacy_policy_page)

        print("\033[92m" + "OK" + "\033[0m")

        print("  Setting up main menu ... ", end="", flush=True)
        menu, _ = MainMenu.objects.get_or_create(site=site)
        MainMenuItem.objects.create(
            link_page=home_page, menu=menu, link_text="Overview"
        )
        MainMenuItem.objects.create(
            link_page=orgs_index, menu=menu, link_text="Organisations"
        )
        MainMenuItem.objects.create(
            link_url="/map", menu=menu, link_text="Map the impact"
        )
        MainMenuItem.objects.create(
            link_page=pubs_index, menu=menu, link_text="Publications"
        )
        MainMenuItem.objects.create(
            link_page=blog_index, menu=menu, link_text="News & Stories"
        )
        MainMenuItem.objects.create(link_page=about_page, menu=menu, link_text="About")

        print("\033[92m" + "OK" + "\033[0m")

        print("  Setting up footer menu ... ", end="", flush=True)
        footer_menu, _ = FlatMenu.objects.get_or_create(
            site=site, title="Footer menu", handle="footer"
        )
        FlatMenuItem.objects.create(
            link_page=about_page, menu=footer_menu, link_text="About"
        )
        FlatMenuItem.objects.create(
            link_page=toc_page, menu=footer_menu, link_text="Terms and conditions"
        )
        FlatMenuItem.objects.create(
            link_page=privacy_policy_page, menu=footer_menu, link_text="Privacy policy"
        )
        FlatMenuItem.objects.create(
            link_page=contact_page, menu=footer_menu, link_text="Contact us"
        )

        print("\033[92m" + "OK" + "\033[0m")

        print("  Adding Superadmin ... ", end="", flush=True)
        create_superuser("admin", "support@matchstick.ug", "ultimate012")
        print("\033[92m" + "OK" + "\033[0m")
