Navigating the CMS
===================================

Once you have logged in successfully, you will be redirected to the Dashboard. 

.. figure:: _static/dashboard.png
    :alt: Data Waffe CMS Dashboard
    :width: 800

Main dashboard
--------------
On the left (dark background) is the Navigation Menu which is used to nagivate to and edit various parts of the CMS. 
At the top of the main section, you can see various numbers summarizing the content hosted on the platform.


You can return to the Dashboard at any time by clicking the round Data Waffe logo in the top left corner.

- The Dashboard shows the number of Pages, images, documents and associated languages currently stored on Wagtail.
- If you are authorized to moderate/review Pages, there will be a list of Pages awaiting your approval. 
  Hovering over the title of the Page will give you several options:

  - Request changes: reject the changes and a comment explaining why
  - Approve: approve the changes and publish the Page
  - Approve with comment: approve the changes and publish the Page, adding a comment
  - Edit: edit the Page yourself
  - Preview: preview the changes on the frontend of the site
  
- If you have recently edited Pages, there will also be a list of your 5 most-recently edited Pages
- Clicking on the title of any Page in the Dashboard will take you to its Edit interface
- Each of the Page lists on the Dashboard also have a status:
  
  - Pages awaiting review will show the review status
  - Pages you have recently edited will show whether it is Live, Draft, or Live + Draft (indicating the Page is published but newer revisions are in a Draft state)

The Pages Menu
-------------------

The Pages Menu enables quick navigation through the levels of the site. Navigation using this menu enables you to move past a navigational level by clicking on the right arrow - or to open a navigational level by clicking its name. You can also navigate back by clicking the name of the containing folder above the list.

The top level of the Pages menu will be the different languages your country’s site is available in. For example, the site shown below is available in English, French and in Swahili.

.. figure:: _static/root-tree.png
    :alt: Root CMS page tree

    Notice the tags on the separate page trees for each language

**Here's what you need to know:**

- Click the Pages button in the sidebar to accesss the Menu.
- Clicking the name of a page will take you to the child pages within that page or to the page edit screen depending on where the page is in the hierachy.
- Clicking the right arrow displays the pages and enables you to navigate through the content structure.
- The more right arrows you click, the further down the content structure you move.

The Pages View
--------------------------

As noted above, the root Pages view contains the different language versions your country site is available in. Any child pages created here will not be accessible from any URL; you must create child pages within an existing site not the root.

.. figure:: _static/root-area.png
    :alt: Root page tree area

    This is the Pages root section. DO NOT CREATE ANY PAGES here.

From the Pages root view, you can navigate to the Homepage of any language site. For the english site, the homepage may have the title: **Welcome**

.. figure:: _static/welcome.png
    :alt: Home page

    This is the homepage for any language and the root of all pages of the rest of the website.


Editing the Homepage
---------------------------------

You can edit the homepage by clicking on the title. Hovering over the title, will also show a menu with other options. 

The editing area allows you to manage all the content as it appears on the homepage including headings, buttons, images, etc. 

.. image:: _static/edit-welcome.png

Managing other pages
-----------------------------

To explore other pages on the website, return to the pages root for any language and click the green arrow (>) in the far right of the Welcome page. This is also how you'll see any child pages for any index page. 

.. image:: _static/other-pages.png

Here you will find the pages that make up the entire website including, index pages (e.g Newsroom page), standard pages (e.g About page) and other custom pages (e.g App download page).

You will notice that all index pages have the green arrow on the far right so you can access the child pages under them e.g Newsroom, Events, Library, Youth Initiatives.

For example, lets look at what lies under the Newsroom page:

.. image:: _static/newsroom-page.png

As you move down through the site, the breadcrumb at the top of the page will display the path you have taken.
In the image above, the breadcrumbs are ‘Great Lakes Youth Network (English)’ > Welcome > Newsroom’. 
Notice that this Page does not contain any further child-pages; all of the content here are Blogs. 

Just below the title of the Page, there are several toolbar buttons, each with a different function that will be explained briefly here, and in more depth in separate sections of this documentation:

- **Edit:** Edit properties of the parent page (in the image above, the “Newsroom” page)
- **View live:** View the live version of the site, as a user would see
- **Add child page:** In this particular case, since we are in the Newsroom Page, this will allow you to add a new blog.
- **More:**
   - **Move:** This will Change the parent page of the currently selected Page (i.e: Newsroom). **DO NOT TOUCH THIS**
   - **Copy:** This will duplicate the current page. **DO NOT TOUCH THIS**
   - **Delete:** Complete delete the current page and all of its child pages(in this case: blogs). **DO NOT TOUCH THIS**
   - **Unpublish:** This option unpublishes the Page and disallows users from accessing it on the live site, optionally disallowing access to child pages (in this case: blogs). Note: if access to child pages is not removed, they will become orphaned meaning that they can be accessed by users, but only through direct URL.
   - **History:** This shows you a log of all the actions taken on this Page.
   - **Translate this page:** This creates a version of this page (and optionally all its child pages) in a different language(locale) if it doesn't exist in that langauge yet.
   - **Sync translated pages:** This will sync all the content on this page into another languages that had already been created to allow the editor manually make translations.
- **Language:** This button allows you to select the language you would like to make edits for. By default this is English. If you select, say French, it will show you the content for the page in French and you can manually translate it here. 

Below the title area and the toolbars defined above, you have a table showing the existing child pages. The columns are self explanatory but lets define them quickly:

.. note::
    You can change the ordering of items in the table by clicking on the column names. This allows you to view the table items in ascending or descending order depending on the column header clicked. 
    You can play with this. It will help you find the pages to edit faster and won't change how they appear on the live site.

Sort:
    When clicked, some grips (six dots) appear to the left of the child page now. These allow you to drag each page item up and down to the desired position or order in the hierachy. The order of the child pages is saved each time you to drag and drop to the desired position in the hierachy. You can stop or exit this action by clicking on Sort again.

    .. note::
        Please note that when creating content pages, the order of these pages on the site Frontend will follow a chronological listing format. 
        For example, the first article you load will remain at the top of the page, with subsequent articles appearing below it. Wagtail allows you to reorder the appearance of Pages. 
        You can individually move them into a new listing position using the Sort button. These appear as two small arrows facing opposite directions to the left of any list of Child pages.

Title:
    The title of the child page.

Updated: 
    The period of time since the page was last updated. 

Type:
    This describes what type of page it is. In the image above, the child pages are all of the type **Blog**

Status:
    This shows you the state of the child page. If a page is published, the status will show as **Live**. Unpublished pages will have the status: **Draft**.


Search Functionality
----------------------------

To quickly locate pages, articles or find information, use the search functionality. This is located in the sidebar of the dashboard, right below the logo. 

**Here's what you need to know:**
- Using Search is an easy way to find the page you’re looking for.
- Simply type in the name of the page you are looking for and hit enter.
- Clicking the title of the page in the results that follow will take you to its edit screen.
- You can filter the search results by content type i.e Page, Image, Document and Users. 
- Different content types have different options for further filtering. Pages can be filtered by Page Type, whereas Images can be filtered by Tags.
- Search results can be sorted by column simply by click on the column header

.. image:: _static/search.png