## What does this do?
This [Automatic1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui) extension allows you to improve your image generation workflow by letting you save the prompt, negative prompt, and seed for selected images you generate so that you can generate them again with higher quality settings.

This allows you to generate massive amounts of low quality images, then select which ones you would like to keep and regenerate them in higher quality all in one go.

Detailed help can be found in the "Keep this prompt for later - Help" expandable section in the scripts section of the Web UI.

## Screenshots
Adds a new "↙️" button in the image gallery

![gallery](https://i.imgur.com/rBkZhxq.jpg)

And the fullscreen image viewer

![fullscreen gallery button](https://i.imgur.com/8ckT4tp.jpg)

Clicking this new button when selecting an image in the gallery will send its prompt, negative prompt, and seed to the textboxes of this script. In this example, we kept two images

![script prompts tab](https://i.imgur.com/FcusSy7.jpg)

Now you change your image generation settings, such as step count and resolution (with Hires fix enabled) to produce higher quality images. Then check "Enable", and click the orange Generate button to create your images.

![config](https://i.imgur.com/n72l72D.jpg)

## Installation
* In your Automatic1111 Web UI, go to the Extensions tab > Install from URL > URL for extension's git repository: `https://github.com/Zyin055/Keep-this-prompt-for-later`
* Click the Install button

## Known bugs
* The progress bar doesn't work correctly with Hires fix enabled
* Doesn't work with newlines in the prompt

## Changelog
<details>
    <summary>Click to view Changelog</summary>

#### 6/02/2024
* Fixed a bug that caused hires prompts to be incorrectly set
* Shows the prompt used to generate the selected image in the image gallery instead of placeholder text
#### 9/01/2023
* Updated for A1111 1.6.0. This version is not backwards compatible with older A1111 versions
* Fixed bug where wrong image is selected if image grids are shown in the web ui
#### 4/28/2023
* Streamlined the UI by removing the scratch paper tab and replacing it with an "Enable" checkbox
* Fixes for the March 28 A1111 update [v1.0.0-pre](https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases/tag/v1.0.0-pre)
#### 1/02/2023
* Button position got moved due to an Automatic1111 update, moved the button back to where it used to be
#### 12/19/2022
* Added 'Enter' as a hotkey for the fullscreen button
#### 12/14/2022
* Initial release
