Image Explorer XBlock
=====================

This XBlock allows to create clickable hotspots on top of a background image.

![Image Explorer Example](https://raw.githubusercontent.com/edx-solutions/xblock-image-explorer/readme-doc/doc/img/image-explorer-example.jpg)

Enabling in Studio
------------------

You can enable the Image Explorer XBlock in studio through the advanced
settings.

1. From the main page of a specific course, navigate to `Settings ->
   Advanced Settings` from the top menu.
2. Check for the `advanced_modules` policy key, and add `"image-explorer"`
   to the policy value list.
3. Click the "Save changes" button.

Usage
-----

When you add the `Image Explorer` component to a course in the studio, the
block is field with default XML content:

```xml
<image_explorer schema_version='1'>
    <background src="//upload.wikimedia.org/wikipedia/commons/thumb/a/ac/MIT_Dome_night1_Edit.jpg/800px-MIT_Dome_night1_Edit.jpg" />
    <description>
        <p>
            Enjoy using the Image Explorer. Click around the MIT Dome and see what you find!
        </p>
    </description>
    <hotspots>
        <hotspot x='370' y='20' item-id='hotspotA'>
            <feedback width='300' height='240'>
                <header>
                    <p>
                        This is where many pranks take place. Below are some of the highlights:
                    </p>
                </header>
                <body>
                    <ul>
                        <li>Once there was a police car up here</li>
                        <li>Also there was a Fire Truck put up there</li>
                    </ul>
                </body>
            </feedback>
        </hotspot>
        <hotspot x='250' y='70' item-id="hotspotB">
            <feedback width='440' height='400'>
                <header>
                    <p>
                        Watch the Red Line subway go around the dome
                    </p>
                </header>
                <youtube video_id='dmoZXcuozFQ' width='400' height='300' />
            </feedback>
        </hotspot>
    </hotspots>
</image_explorer>
```

The wrapping `<image_explorer>` contains the following child elements:

* `<background>` - Contains the URL of the background image to display, as a `src` argument.
* `<description>` - Contains the description of the exercise, and can contain arbitrary HTML.
* `<hotspots>` - Contains the individual `<hotspot>` children, one for each hotspot to display
  on top of the background image

Each `<hotspot>` has the following attributes:

* `x` - The horizontal position of the hotspot
* `y` - The vertical position of the hotspot
* `item-id` - A unique id used to reference the hotspot.

Each `<hotspot>` can contain a `<feedback>` child element, which contains the HTML of the message
to display to the user when the hotspot is clicked. It also contains `width` and `height` attributes,
which provide the size of the feedback popup used to display the message.

