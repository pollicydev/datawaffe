Creating content
===================================

The GLYN website handles content in multiple languages i.e English, French and Swahili. This CMS was built to manage
this content in the most robust manner. All the content is translatable and the website has been developed to show
content available based on the language selected on the frontend. 

.. note::
    The default language for all page content is English. From this, all content is synced across the Page trees of other languages.
    If anything has not been translated yet, it will appear in English even though the user has chosen say French as their language.

Editing existing pages
-------------------------



Managing Edit Tabs
-------------------------
A common feature of the *Edit* pages for all page types is the three tabs at the top of the screen. The first, *Content*, is where you build the content of the page itself.

The Promote tab
-----------------------

The Promote tab is where you can configure a page's metadata, to help search engines find and index it. Below is a description of all the default fields under this tab.

**For Search Engines**

* **Slug:** The section of the URL that appears after your website's domain e.g. ``http://greatlakesyouth.africa/blog/[my-slug]/``. This is automatically generated from the main page title, which is set in the Content tab. Slugs should be entirely lowercase, with words separated by hyphens (-). It is recommended that you don't change a page's slug once a page is published.

* **Page title:** This is the bold headline that often shows up search engine results. This is one of the most significant elements of how search engines rank the page. The keywords used here should align with the keywords you wish to be found for. If you don't think this field is working, ask your developers to check they have configured the site to output the appropriate tags on the frontend.

**For Site Menus**

* **Show in menus:** Ticking this box will ensure that the page is included in automatically generated menus on your site. Note: A page will only display in menus if all of its parent pages also have *Show in menus* ticked.

* **Search description:** This is the descriptive text displayed underneath a headline in search engine results. It is designed to explain what this page is about. It has no impact on how search engines rank your content, but it can impact on the likelihood that a user will click your result. Ideally 140 to 155 characters in length. If you don't think this field is working, ask your developers to check they have configured the site to output the appropriate tags on the frontend.

* **Search image**: Upload an image that will appear alongside the link in search results or when the link to this page is shared on social media. 


.. image:: _static/promote-tab.png

.. Note::
    You may see more fields than this in your promote tab. These are just the default fields, but you are free to add other fields to this section as necessary.

The Settings Tab
--------------------------

The *Settings* tab has three fields by default.

* **Go Live date/time:** Sets the date and time at which the changes should go live when published. 
* **Expiry date/time:** Sets the date and time at which this page should be unpublished.
* **Privacy:** Sets restrictions for who can view the page on the frontend. Also applies to all child pages.



Creating Blogs/Articles
-----------------------------

There are three core components of a Blog page:

* **Title:** The title of the article
* **Summary:** A brief summary of the content in the blog. There's a limit on the number of characters.
* **Featured image:** The image associated with the blog wherever it appears. 
* **Featured video:** A video associated with the blog. This has to be the 11 character code at the end of the link to an existing video on the GLYN YouTube channel.
* **Blog Text:** This is the main content of the blog or article. Take advantage of the various blocks to create a better experience. The paragraph block gives you access to an editing experience similar to that of any word editor. The blockquote block allows you to create quotes that can be embedded in between paragraph blocks. The embed block is good for embedding videos in between paragraph blocks.
* **Add images to Gallery:** This is only necessary if you need to have a gallery of images within the blog or article. This is usually necessary for event updates when you need to show images of what happened at an event along with the update.

.. note:: 
    A featured image is compulsory. However, if a featured video is availed - on the blog page on the live site, the video will appear instead of the featured image or image gallery (if availed).
    The featured image will appear everywhere else. 



Uploading and adding images
----------------------------

There are two places where you can use images in your pages or articles:

* **Featured images:** These appear beside or atop the page or article wherever it appears.
* **In-body images:** These appear in the paragraph text when added through an editor.

**Adding Featured images**

Navigate to the page or blog you to wish add a featured image to (provided the option exists on the edit screen). 
On the Image are, you will see a button with the text: **Choose an image**

.. image:: _static/choose-image.png

On clicking this, a "choose an image" dialog will pop up with two tabs: Search and Upload. 

The search tab allows you to select an image from the existing images already uploaded to the website. Click any image to select it.

.. image:: _static/search-images.png

The upload tab allows you to select an image from your computer and upload an image to the GLYN media server to use it in your page or blog. 

.. image:: _static/upload-image.png

After adding an image, you will be presented with three buttons beside the image:

.. image:: _static/featured-image.png

* **Clear choice:** Remove the selected image from the page or article. Image area will be left blank
* **Change image:** Pops up the "choose an image" dialog so you can select another image to replace the current one.
* **Edit image:** Change the image metadata such as its title, and among other things, you can also choose a focal point on the image. Whenever the image is used, the focal point will always be visible.

**Adding In-body images**

Navigate to the paragraph block on any page or blog where you would like to add the image. Put the cursor where you want to place the image. 
In the toolbar above the input area, you will see an image icon, selecting it will popup the "choose an image" dialog that allows you to find
an existing image to add or to upload a new image from your computer. 

.. image:: _static/paragraph-image.png

Uploading and adding documents
----------------------------------

You will encounter this option when trying to add resources to the library. The flow is similar to that of addding images above. 
The prompts will change to "choose a document". You can also attach documents within paragraphs in a similar way to adding images as defined above.
The only difference is the icon you select in the edit toolbar is that of a piece of paper. 

Previewing and submitting pages for moderation
-------------------------------------------------

.. image:: _static/page-submit.png 

The Save/Preview/Submit for moderation menu is always present at the bottom of the page edit/creation screen. The menu allows you to perform the following actions, dependent on whether you are an editor, moderator or administrator:

* **Save draft:** Saves your current changes but doesn't submit the page for moderation and so wonâ€™t be published. (all roles)
* **Submit for moderation:** Saves your current changes and submits the page for moderation. The page will then enter a moderation workflow: a set of tasks which, when all are approved, will publish the page (by default, depending on your site settings). This button may be missing if the site administrator has disabled moderation, or hasn't assigned a workflow to this part of the site.  (all roles)
* **Preview:** Opens a new window displaying the page as it would look if published, but does not save your changes or submit the page for moderation. (all roles)
* **Publish/Unpublish:** Clicking the *Publish* button will publish this page. Clicking the *Unpublish* button will take you to a confirmation screen asking you to confirm that you wish to unpublish this page. If a page is published it will be accessible from its specific URL and will also be displayed in site search results. (moderators and administrators only)
* **Delete:** Clicking this button will take you to a confirmation screen asking you to confirm that you wish to delete the current page. Be sure that this is actually what you want to do, as deleted pages are not recoverable. In many situations simply unpublishing the page will be enough. (moderators and administrators only)

Translating pages
-------------------------------------------------

Once you have created and published content for any page, aliases of those pages will automatically be created in the French and Swahili versions.
All the other locales: French and Swahili sync from the English version. 

At the moment of publishing, the French and Swahili pages are an exact copy of the English pages. So for learning purpose, lets translate them into French!

To translate the blog post you just created, find the French language of it in the page explorer and click edit. Alternatively, you can go straight from editing the English version to the French using the language selector at the top of the editor.

When you get to the edit view, you will get this message (this is because it is keeping itself in sync with the English page):

.. image:: _static/wagtail-translate-page.png 

Hit that "Translate this page" button, then click "Submit" on the step afterwards, this will put the page into translation mode, and the editor should now look something like this:

.. image:: _static/wagtail-edit-translation.png 

As you can see, each segment of translatable text has been extracted into a separate editable block. Translating in this way makes it easier to keep the translations in sync with the original page, as editors only need to retranslate changed segments when the original page is updated.