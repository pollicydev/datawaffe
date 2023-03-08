Definitions
===================================

There are several terms and concepts that you will find throughout the Data Waffe CMS. These terms are presented here:

CMS:
    Abbreviation for “Content Management System”. A CMS is any software that helps manage the creation 
    and modification of digital content, such as articles, images, videos, and documents and even users.

Django:
    Django is a free and open-source software library written in Python that is used to create web applications.

Wagtail:
    Wagtail is a free and open-source CMS for Django.

Data Waffe CMS:
    Data Waffe uses python underneath the hood and takes advantage of Wagtail, Django frameworks, and other languages to deploy a platform that can scales with the needs of its users. 
    Throughout this documentation, this software solution will be referred to as “the Data Waffe CMS”, or more simply as “the CMS”.

Dashboard:
    The initial view immediately after logging into the CMS. Displays the Pages, Images, Documents, and Media files currently loaded on the site, 
    as well as your recently edited Pages and any Pages that are awaiting review.

Page:
    In the Data Waffe CMS, the Page is the simplest form of presenting content. There are different variations of the Page. 
    Each has different use cases. See “Page Types” below for a list of different Page variations.

Page Types:
    Pages can be any one of the following types:
        - Home page
        - Standard page
        - Organisation page
        - Blog page
        - Publication page
        - Form page
        - Index page

    Home page:
        This is the content on the landing page located at https://datawaffe.org. All other pages on the website are descendants of this page.

    Standard page:
        A standard page is used to create general content pages. They have no structure and all their formatting can be done in the editor. 
        Examples include: the `Privacy Policy`_ page.

        .. _Privacy Policy: https://datawaffe.org/privacy/

    Organisation page:
        Organisation pages are the life and blood of this platform. Every organisation is a member of `Uganda Key Populations Consortium (UKPC)`_ Most of the data on this platform is aggregated from multiple organisations. You will learn how
        to setup pages for each organisation in the subsequent pages. All Organisation pages are descendants of the `Organisation Index Page`_.

        .. _Uganda Key Populations Consortium (UKPC): https://ugandakpc.org
        .. _Organisation Index Page: https://datawaffe.org/organisations

    Blog page:
        Blog pages are used to create articles usually known as blogs. They primarily consist of a title, excerpt, formatted body text and a featured image. 
        Blog pages are descendants of the `Blog index page`_

        .. _Blog Index Page: https://datawaffe.org/blog/

    Publication page:
        Publication pages are essentially public documents. This can be research, advocacy briefs or policy instruments. They have to be properly tagged and assigned
        to the publishing organisation. All Publication pages are descendants of the `Publication Index Page`_.

        .. _Publication Index Page: https://datawaffe.org/publication/

    Form page:
        A Form Page is any page that is designed to hold a form and collect user information or feedback. Data Waffe has only one form page: The `Contact page`_ which
        allows users to share any concerns or constructive feedback.

        .. _Contact page: https://datawaffe.org/contact/

    Index page:
       We have mentioned index pages a lot in the definitions section. Index Pages are a special type of Page that can only exist as the direct child of the Homepage. 
       They are similar to folders on your operating system, but can only contain one type of Child Page. For example, all blogs will go into a Blog Index Page. 
       Similarly, all organisations go under a Organisation Index Page. 
       
       Most platforms like Data Waffe are typically organized as Homepage > Index Page > Child