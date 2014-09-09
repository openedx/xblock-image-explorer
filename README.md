Image Explorer XBlock
=====================

This package provides the Image Explorer XBlock that allows you to
use an image with hotspots in a course. When the student clicks a
hotspot icon, tooltip containing custom content is displayed.

Screenshot below shows the Image Explorer XBlock rendered inside the
edX LMS with an activated tooltip containing and embedded YouTube video.

![Student view](https://raw.githubusercontent.com/edx-solutions/xblock-image-explorer/3b67392a73edcd606f4e3fb30cfa8b3cc20720d3/doc/img/student-view.png)

Installation
------------

Install the requirements into the python virtual environment of your
`edx-platform` installation.

```bash
$ pip install -r requirements.txt
```

Enabling in Studio
------------------

You can enable the Image Explorer XBlock in studio through the
advanced settings.

1. From the main page of a specific course, navigate to `Settings ->
   Advanced Settings` from the top menu.
2. Check for the `advanced_modules` policy key, and add
   `"image-explorer"` to the policy value list.
3. Click the "Save changes" button.

Usage
-----

When you add the `Image Explorer` component to a course in the studio,
the block is field with default content, shown in the screenshot below.

![Edit view](https://raw.githubusercontent.com/edx-solutions/xblock-image-explorer/3b67392a73edcd606f4e3fb30cfa8b3cc20720d3/doc/img/edit-view.png)

The basic structure of the `image_explorer` XBlock looks like this:

```xml
<image_explorer schema_version="1">
  <background src="http://link/to/image.jpg" />
  <description>...custom HTML content...</description>
  <hotspots>
    <hotspot x="370" y="20">
      <feedback width="300" height="300">
        <header>...custom HTML content...</header>
        <body>...custom HTML content...</body>
        <youtube video_id="dmoZXcuozFQ" width="400" height="300" />
      </feedback>
    </hotspot>
    <hotspot>...</hotspot>
    ...
    <hotspot>...</hotspot>
  </hotspots>
</image_explorer>
```

The `schema_version` attribute of the `<image_explorer>` wrapper
element should be set to `1`. It currently isn't used but will provide
help for easier schema migrations if the XML schema changes in future
versions.

The `<image_explorer>` element should contain the following child
elements:

* `<background>` (required)
* `<description>` (optional)
* `<hotspots>` (required)

### The background element

The `src` attribute of the `<background>` element defines the image
over which the hotspots are placed.

### The description element

The optional `<description>` element can contain arbitrary HTML
content that is rendered above the image.

### The hotspots element

The `<hotspots>` element wraps an arbitrary number of child
`<hotspot>` elements. These define the position of the hotspots on the
background image and the content of the tooltips.

The supported attributes of `<hotspot>` elements are `x` and `y` (both
required) that specify the position of the hotspot on the background
image, `item-id` which can be set to a unique string used to
identify the hotspot in the emitted events and optional `side` attribute 
that allows to override hotspot's popup position. If `side` attribute is 
missing or set to anything except `left` and `right` automatic positioning
is used.

Each `<hotspot>` element must contain the `<feedback>` child
element. The `<feedback>` element supports `width`, `height` and `max-height`
attributes (all optional) that specify the dimensions of the tooltip
element. The default width is `300px` and if no height is specified, the
max-height is set to `500px`. So the content will be sized dynamically with a
vertical scrollbar for the overflow.

The `<feedback>` element can contain the following child elements:

* `<header>`
* `<body>`
* `<youtube>`

#### The header element

If present, the `<header>` specifies the tooltip header. It may
contain arbitrary HTML content.

#### The body element

The `<body>` element can contain arbitrary HTML content that is
rendered in the tooltip.

#### The youtube element

The `<youtube>` element offers a convenient way of placing an embedded
YouTube video into a tooltip. The required attributes are `video_id`,
`width`, and `height`.

License
-------

The Image Explorer XBlock is available under the GNU Affero General
Public License (AGPLv3).
