## Add to List

Adds the input item to the given list.

Even though the description says this action accepts input of type Files, it accepts any type.

Note: If you get the error “The operation failed because Shortcuts couldn't convert from Text to NSString.”, just change the preview to show a list view instead. This is a bug in the Shortcuts app.

### Parameters

- **List** (Array of File)
- **Item** (File)
- **Prepend** (Boolean)

### Returns

Array of File

---

## Apply Capture Date

Applies the original capture date and time of the photo (from Exif metadata) to the file's creation and modification date.

If an image does not have a capture date metadata, the file is just passed through.

This action can be useful to run after the built-in “Convert Image” action (ensure “Preserve Metadata” is checked).

### Parameters

- **Images** (Array of File)
- **Also Set Modification Date** (Boolean)

### Returns

Array of File

---

## Ask for Text with Timeout

Displays a dialog prompting the user to enter some text.

If you provide a timeout, the action will cancel after the given timeout as long as the user has not started writing anything.

IMPORTANT: The result is copied to the clipboard. Add the “Wait to Return” and “Get Clipboard” actions after this one.

### Parameters

- **Prompt** (Text)
- **Type** (`InputTypeAppEnum`)
- **Message** (Text)
- **Default Answer** (Text)
- **Timeout** (Measurement of UnitDuration)
- **Return Value on Timeout** (Text)
- **Show Cancel Button** (Boolean)

---

## Authenticate

Authenticate the user using Face ID or Touch ID.

Unlike the old authenticate action, this one directly returns a boolean for whether the authentication succeeded.

On iOS & visionOS, it needs to momentarily open the Actions app to be able to present the authentication prompt. Afterwards, it goes back to the Shortcuts app. If you were running the shortcut in the background, there is unfortunately no way to go back to the previous app you were in, other than opening the app again from the shortcut.

### Parameters

- **Open When Authenticated** (URL)
- **Timeout (seconds)** (Double)

### Returns

Boolean

---

## Authenticate (Legacy)

Authenticate the user using Face ID or Touch ID.

IMPORTANT: Use the “Authenticate” action instead.

IMPORTANT: The result is copied to the clipboard as the text “true” or “false”. Add the “Wait to Return” and “Get Clipboard” actions after this one. Use the “If” action to decide what to do with the result.

Q: Why can't it return the value directly?
A: The system authentication feature can only be triggered from an app, so the action has to send you to the Actions app, which shows it, and then sends you back to the shortcut.

### Parameters

- **Open When Finished** (URL)
- **Timeout (seconds)** (Double)

---

## Blur Images

Apply gaussian blur to the input images.

### Parameters

- **Images** (Array of File)
- **Amount** (Double)

### Returns

Array of File

---

## Boolean

Passes the specified boolean value to the next action.

Similar to the built-in “Number” and “Text” actions.

This can be useful if you want to create a variable that is initially set to a boolean.

Note that event though the preview shows a localized word, the actual value is always the same, a boolean.

### Parameters

- **Boolean** (Boolean)

### Returns

Boolean

---

## Calculate with Soulver

Lets you calculate day-to-day math expressions using natural language, provided by Soulver.


Examples:

$10 for lunch + 15% tip
→ $11.50

65 kg in pounds
→ 154.32 lb

$2 in euro
→ €2,02

12% of 478
→ 57.36

40 as % of 90
→ 44.44%

$150 is 25% on what
→ $120.00

$25/hour * 14 hours of work
→ $350.00

January 30 2020 + 3 months 2 weeks 5 days
→ May 19, 2020

9:35am in New York to Japan
→ 10:35 pm

days until April
→ 37 days

days left in Feb
→ 5 days

days remaining in 2023
→ 311 days

$25k over 10 years at 7.5%
→ $51,525.79 (compound interest)


The expression can be written in English, German, Russian, or Simplified Chinese.

If you like this action, you may also like the Soulver macOS app.

### Parameters

- **Expression** (Text)
- **Decimal Places** (Number)
- **Show Thousands Separator** (Boolean)
- **Abbreviate Large Numbers** (Boolean)
- **Use Live Currency Rates** (Boolean)

### Returns

Text

---

## Choose from List (Extended)

Presents a searchable list where you can select one or multiple items.

It also supports setting a timeout and interactively adding custom items.

This is an extended version of the built-in “Choose from List” action.

IMPORTANT: Add the “Wait to Return” and “Get Clipboard” actions after this one.

NOTE: It will convert each input into a string, so some types may not work properly.

Note: If you get the error “The operation failed because Shortcuts couldn't convert from Text to NSString.”, just change the preview to show a list view instead. This is a bug in the Shortcuts app.

### Parameters

- **List** (Array of Text)
- **Prompt** (Text)
- **Message** (Text)
- **Select Multiple** (Boolean)
- **Select All Initially** (Boolean)
- **Allow Custom Items** (Boolean)
- **Use Timeout** (Boolean)
- **Timeout** (Measurement of UnitDuration)
- **Return Value on Timeout** (`ChooseFromListTimeoutValueAppEnum`)

---

## Clamp Number

Clamps the input number to above or equal to the given minimum number and below or equal to the given maximum number.

For example, if you provide 10 as the number, 4 as minimum, and 8 as maximum, you will get 8 back.

### Parameters

- **Number** (Double)
- **Minimum** (Double)
- **Maximum** (Double)

### Returns

Double

---

## Color

Create a color type.

This color type can be used as input for the following actions:
- Pick Color
- Get Average Color

This color type is the return value of the following actions:
- Pick Color
- Get Random Color
- Get Dominant Colors of Image
- Get Average Color of Image

For example, you could get the two most dominant colors of an image using the “Get Dominant Colors of Image” action and then pass the result into the “Get Average Color” action to get the average of those.

### Parameters

- **Color (hex format)** (Text)
- **Set Opacity** (Boolean)
- **Opacity** (Double)

### Returns

`ColorAppEntity`

---

## Combine Lists

Combines two or more lists into one list.

Supports up to 10 lists.

Tap and hold a list parameter to select a variable to a list. Don't quick tap it.

Note: If you get the error “The operation failed because Shortcuts couldn't convert from Text to NSString.”, just change the preview to show a list view instead. This is a bug in the Shortcuts app.

### Parameters

- **List 1** (Array of File)
- **List 2** (Array of File)
- **List 3** (Array of File)
- **List 4** (Array of File)
- **List 5** (Array of File)
- **List 6** (Array of File)
- **List 7** (Array of File)
- **List 8** (Array of File)
- **List 9** (Array of File)
- **List 10** (Array of File)

### Returns

Array of File

---

## Combine Videos

Combine videos into a single video.

IMPORTANT: The videos must have the same size and orientation.

This can be useful for combining Live Photos.

It uses passthrough whenever possible to prevent unnecessary transcoding, preserving original video quality.

NOTE: On iOS & visionOS, shortcut actions only get 30 seconds to run, so if the videos are very long, it may not work.

### Parameters

- **Videos** (Array of File)

### Returns

File

---

## Convert Coordinates to Location

Returns the location at the given latitude and longitude.

Tip: Use the built-in “Get Details of Locations” action to get more details from the location.

### Parameters

- **Latitude** (Double)
- **Longitude** (Double)

### Returns

Location

---

## Convert Date to Unix Time

Returns the Unix time for the input date.

Example: 1663178163

Tip: Write “current date” as the date to get it for the current date and time.

Unix time (also known as Epoch time) is a system for describing a point in time — the number of seconds that have elapsed since the Unix epoch.

### Parameters

- **Date** (Date)

### Returns

Number

---

## Convert Location to Geo URI

Returns the geo URI for the given location.

### Parameters

- **Location** (Location)
- **Include Accuracy** (Boolean)

### Returns

URL

---

## Convert Unix Time to Date

Returns the date for the input Unix time.

Unix time (also known as Epoch time) is a system for describing a point in time — the number of seconds that have elapsed since the Unix epoch.

### Parameters

- **Unix Time** (Number)

### Returns

Date

---

## Create Color Image

Creates a solid color image.

### Parameters

- **Hex Color** (Text)
- **Width** (Number)
- **Height** (Number)
- **Opacity** (Double)

### Returns

File

---

## Create Menu Item

Create a menu item with a title, subtitle, and icon.

You can later use one or more of these menu items in a “Choose from List” action.

Add an “Add to Variable” action below this one to populate a list and then use that variable in the “Choose From List” action.

### Parameters

- **Title** (Text)
- **SF Symbol** (Text)
- **Emoji** (Text)
- **Subtitle** (Text)
- **Icon Type** (`MenuItemIconType`)
- **Foreground Color** (`MenuItemStyle`)
- **Custom Foreground Color (Hex)** (Text)
- **Background Color** (`MenuItemStyle`)
- **Custom Background Color (Hex)** (Text)
- **Background Style** (`MenuItemBackgroundShape`)
- **Data** (Text)

### Returns

`MenuItem`

---

## Create Notification Action

Creates a notification action to be used in the “Actions” parameter of the “Show Notification” action.

### Parameters

- **Title** (Text)
- **URL to Open** (URL)
- **Icon (SF Symbol)** (Text)
- **Is Destructive** (Boolean)

### Returns

`NotificationAction_AppEntity`

---

## Create URL

Creates a URL from components.

### Parameters

- **Scheme** (Text)
- **Host** (Text)
- **Path** (Text)
- **Query Items (every other item is key & value)** (Array of Text)
- **Fragment** (Text)
- **User** (Text)
- **Password** (Text)
- **Custom Port** (Boolean)
- **Port** (Number)

### Returns

URL

---

## Debug (Internal)

This is meant for debugging problems with actions.

### Returns

Text

---

## Download File

Downloads the file at the given URL.

This action is beneficial over the built-in “Get Contents of URL” because it doesn't show a privacy prompt for each new host.

NOTE: It only works for HTTPS URLs, not HTTP.

IMPORTANT: On iOS, it can run for a maximum of 25 seconds. It's suitable only for smaller downloads that can complete within this timeframe.

### Parameters

- **URL** (URL)

### Returns

File

---

## Edit URL

Lets you edit the components of the input URL.

For example, add a query item, change the path, or remove the fragment.

### Parameters

- **URL** (URL)
- **Action** (`EditURLActionAppEnum`)
- **Name** (Text)
- **Value** (Text)
- **Path Component** (Text)
- **Query** (Text)
- **Fragment** (Text)
- **Name** (Text)
- **Username** (Text)
- **Password** (Text)
- **Query** (Text)
- **Fragment** (Text)
- **Path** (Text)
- **Scheme** (Text)
- **Host** (Text)

### Returns

URL

---

## Encrypt File

Encrypts/decrypts a file/data securely using the given key.

IMPORTANT: Don't store the key in the shortcut if you intend to share the shortcut. Instead, read it from a local file.

See the “Encrypt Text” action to encrypt text.

The encryption/decryption is performed on-device. Nothing leaves the device.

It uses AES-256-GCM encryption with a randomly generated 12-byte nonce. The encrypted data consists of the nonce (12 bytes), the ciphertext, and the authentication tag (16 bytes), concatenated together in that order. This combined data is then Base64-encoded. There is no padding used in AES-GCM.

### Parameters

- **Action** (Boolean)
- **File** (File)
- **Key** (Text)
- **Decrypted Type** (Text)

### Returns

File

---

## Encrypt Text

Encrypts/decrypts text securely using the given key.

The encrypted text is returned as Base64-encoded text.

IMPORTANT: Don't store the key in the shortcut if you intend to share the shortcut. Instead, read it from a local file.

See the “Encrypt File” action to encrypt things like files and images.

The encryption/decryption is performed on-device. Nothing leaves the device.

It uses AES-256-GCM encryption with a randomly generated 12-byte nonce. The encrypted data consists of the nonce (12 bytes), the ciphertext, and the authentication tag (16 bytes), concatenated together in that order. This combined data is then Base64-encoded. There is no padding used in AES-GCM.

### Parameters

- **Action** (Boolean)
- **Text** (Text)
- **Key** (Text)

### Returns

Text

---

## Filter List

Choose which items to keep or discard in the input list based on a condition.

Note: If you get the error “The operation failed because Shortcuts couldn't convert from Text to NSString.”, just change the preview to show a list view instead. This is a bug in the Shortcuts app.

### Parameters

- **List** (Array of Text)
- **Keep** (Boolean)
- **Condition** (`FilterConditionAppEnum`)
- **Text** (Text)
- **Case Sensitive** (Boolean)
- **Limit** (Boolean)
- **Maximum Results** (Number)

### Returns

Array of Text

---

## Flash Screen

Flashes the screen momentarily.

---

## Format Currency

Formats the input amount as currency.

### Parameters

- **Amount** (Double)
- **Currency** (`CurrencyAppEntity`)

### Returns

Text

---

## Format Date Difference

Formats the difference of one date relative to another date.

For example, “Yesterday” or “2 weeks ago”.

### Parameters

- **First Date** (Date)
- **Second Date** (Date)

### Returns

Text

---

## Format Duration

Formats the input duration to a human-friendly representation.

For example, “9h 41m 30s” or “9:31:30”.

Styles:
- Positional: 9:31:30
- Abbreviated: 9h 41m 30s
- Brief: 9hr 41min 30sec
- Short: 9 hr, 41 min, 30 sec
- Full: 9 hours, 41 minutes, 30 seconds
- Spell Out: nine hours, forty-one minutes, thirty seconds

### Parameters

- **Duration** (Double)
- **Unit Style** (`FormatDurationUnitStyleAppEnum`)
- **Show Seconds** (Boolean)
- **Show Minutes** (Boolean)
- **Show Hours** (Boolean)
- **Show Days** (Boolean)
- **Show Months** (Boolean)
- **Show Years** (Boolean)
- **Maximum Unit Count** (Number)

### Returns

Text

---

## Format Number as Ordinal

Converts the given number to its ordinal form.

For example, 1 becomes “1st”, 2 becomes “2nd”, and 5678 becomes “5678th”.

### Parameters

- **Number** (Number)
- **Locale** (`LocaleAppEntity`)

### Returns

Text

---

## Format Number — Compact

Formats the number into text using a compact style.

For example, 3420 becomes “3.4 thousand” or “3.4K”.

### Parameters

- **Number** (Double)
- **Abbreviated Unit** (Boolean)

### Returns

Text

---

## Format Person Name

Formats the name of a person.

### Parameters

- **Given Name** (Text)
- **Middle Name** (Text)
- **Family Name** (Text)
- **Name Prefix** (Text)
- **Nickname** (Text)
- **Style** (`FormatPersonNameStyleAppEnum`)

### Returns

Text

---

## Generate CSV

Generates a CSV file from a list of dictionaries.

The keys of the dictionaries are the CSV headers.

The dictionaries must have the same shape.

### Parameters

- **Dictionaries** (Array of File)
- **Keys** (Array of Text)
- **Delimiter** (`CSVDelimiterAppEnum`)
- **Custom Delimiter** (Text)

### Returns

File

---

## Generate Haptic Feedback

Generate haptic feedback (vibrate).

The action has to momentarily open the main app as haptic feedback can only be generated from the app.

Not supported on i​Pad. Requires i​Phone 8 or later.

On macOS and visionOS, it does nothing.

### Parameters

- **Type** (`HapticFeedbackTypeAppEnum`)

---

## Generate Random Data

Generates cryptographically secure random data as Hex, Base64, or binary.

Example use-cases: Generating keys, secrets, nonces, OTP, passwords, PINs, secure tokens, etc.

### Parameters

- **Size** (Number)
- **Type** (`GenerateRandomDataOutputTypeAppEnum`)

### Returns

File

---

## Generate Random Text

Generates random text of the given length.

This can be useful as a placeholder, token, etc.

### Parameters

- **Length** (Number)
- **Lowercase** (Boolean)
- **Uppercase** (Boolean)
- **Digits** (Boolean)
- **Use Custom Characters** (Boolean)
- **Custom Characters** (Text)
- **Seed** (Text)

### Returns

Text

---

## Generate UUID

Generates a universally unique identifier (UUID).

### Returns

Text

---

## Get Actions App Version

Returns the current version of the Actions app.

The build number is an increasing integer and can be used to do version checks.

### Returns

`ActionsVersionAppEntity`

---

## Get Audio Playback Destination (Does not detect AirPlay devices)

Returns the audio playback destination of the device.

Can be useful in combination with the built-in “Set Playback Destination” action.

Known limitation: It will not be able to detect when the output is an AirPlay device because of a system bug.

### Returns

Text

---

## Get Average Color

Returns the average color of the input colors.

IMPORTANT: Because of a bug in the Shortcuts app, you must first make the colors you want with the “Color” action, then pass the colors to the “List” action, and then pass the list to this action. (If you work at Apple → FB13291593)

### Parameters

- **Color** (Array of `ColorAppEntity`)

### Returns

`ColorAppEntity`

---

## Get Average Color of Image

Returns the average color of the image.

Average color is all the colors in an image mixed into one, while dominant color is the most seen color in an image.

### Parameters

- **Image** (File)

### Returns

`ColorAppEntity`

---

## Get Battery State

Returns whether the device's battery is unplugged, charging, or full.

### Parameters

- **State** (`BatteryStateTypeAppEnum`)

### Returns

Boolean

---

## Get Bluetooth Device

Returns the Bluetooth device with the given identifier if it's in range and discoverable.

This can be useful to check if a certain Bluetooth device is connected or in range and perform a specific action based on that.

Use the “Get Bluetooth Devices” action to discover devices and their identifiers.

NOTE: You need to allow the Bluetooth permission in the main app before using this action.

NOTE: You need to have been connected to the device at least once before.

NOTE: It only works for BLE (Bluetooth Low Energy) peripherals, not legacy Bluetooth peripherals.

NOTE: Bluetooth has a lot of limitations on iOS and if this action doesn't work for you, it's unfortunately unlikely there is anything I can do about it.

NOTE: The `transmitPowerLevel` property is not provided for this action.

NOTE: The RSSI and signal strength are available for only one of the two AirPods. If it shows RSSI of 0, try the identifier of the other AirPods device.


> Can you support diconnecting from a device?
  Third-party apps like Actions cannot disconnect Bluetooth devices. This is an iOS limitation.

### Parameters

- **Device Identifier** (Text)
- **Timeout (seconds)** (Double)

### Returns

`BluetoothDevice_AppEntity`

---

## Get Bluetooth Devices

Returns the Bluetooth devices in range.

DO NOT COPY THE IDENTIFIER FROM THE PREVIEW. Shortcuts sometimes adds an extra dash. Instead, fetch the "identifier" property.

On iOS & visionOS, it has to open the main app while scanning because they do not allow scanning for arbitrary devices in the background.

Use the “Get Bluetooth Device” action to check for a specific device.

NOTE: You need to allow the Bluetooth permission in the main app before using this action.

NOTE: The “connected” status may not be correct. For a correct connection status, use the “Get Bluetooth Device” action.

NOTE: The “Services” field is only available in the “Get Bluetooth Device” action.

### Parameters

- **Scan Duration (seconds)** (Double)
- **Include Unnamed Devices** (Boolean)

### Returns

Array of `BluetoothDevice_AppEntity`

---

## Get Boolean from Input

Converts boolean-like text values (for example, “true”, “yes”, “on”, “1”) into their corresponding boolean representation.

If no boolean could be detected, it returns an empty result.

This can be useful when an action expects a proper boolean type and you only have some boolean-like text value.

### Parameters

- **Boolean-like Text** (Text)

### Returns

Boolean

---

## Get Compass Heading

Returns the current compass heading, in magnetic or true north format.

The returned value is in degrees. The value 0 means the device is pointed toward north, 90 means it is pointed due east, 180 means it is pointed due south, and so on.

Magnetic heading aligns with traditional compasses and maps, while true north is crucial for accurate astronomical alignments and specific surveying tasks.

NOTE: Does not work on visionOS.

### Parameters

- **Heading Type** (`CompassHeadingType_AppEnum`)

### Returns

Double

---

## Get Default Printer

Returns the default printer.

### Returns

`PrinterAppEntity`

---

## Get Device Details (Extended)

Get details about the device.

This is an extension to the built-in “Get Device Details” action. Unlike the built-in action, this one returns all the values at once instead of making you pick a single value in the action.

You can access the individual values. For example, with the built-in “Show Result” action.

Possible values for thermal state: Nominal, Fair, Serious, Critical

Tip: Use the “Format Duration” action to format the “Uptime” and “Duration since boot” values.

### Returns

`DeviceDetailsAppEntity`

---

## Get Device Motion Data

Returns measurements of the acceleration, rotation rate, and attitude of the device.

Data:
- User Acceleration: Acceleration that the user is giving to the device.
- Gravity: Gravity acceleration vector expressed in the device's reference frame.
- Rotation Rate: Bias-corrected gyroscope data measuring rotation around three axes.
- Attitude: Orientation of the device relative to the device's reference frame.
	- Roll: Rotation around a longitudinal axis that passes through the device from its top to bottom.
	- Pitch: Rotation around a lateral axis that passes through the device from side to side.
	- Yaw: Rotation around its vertical axis, originating at its center of gravity and directed downwards.
	- Quaternion: Orientation in 3D space as a quaternion, providing a compact and efficient way to describe its rotation relative to the device's reference frame.

Google “CMDeviceMotion” for more info about this data.

Use the built-in “Show Result” action to inspect the individual properties.

NOTE: On iOS, the action can only run for maximum 30 seconds, so the interval times sample count must be less than that.

NOTE: Does not work on visionOS.

### Parameters

- **Sample Count** (Number)
- **Interval (seconds)** (Double)

### Returns

Array of `DeviceMotion_AppEntity`

---

## Get Device Orientation

Returns the orientation of the device.

For example, whether the device is portrait or facing down.

Possible values:
- unknown
- portrait
- portraitUpsideDown
- landscapeLeft
- landscapeRight
- faceUp
- faceDown

On macOS and visionOS, it always returns “unknown”.

---

## Get Dominant Colors of Image

Returns the dominant colors of the image.

You could use this to make a palette of the main colors in an image.

Dominant color is the most seen color in an image, while average color is all the colors in an image mixed into one.

Note: The Shortcuts output preview is buggy and shows the colors in random order. Switch to the list view for a stable order in the preview.

### Parameters

- **Image** (File)
- **Count** (Number)
- **Exclude White** (Boolean)
- **Exclude Black** (Boolean)

### Returns

Array of `ColorAppEntity`

---

## Get Emojis

Returns all emojis in the input text.

### Parameters

- **Text** (Text)

### Returns

Text

---

## Get File Icon

Returns the icon for the input files or directories.

### Parameters

- **Files** (Array of File)

### Returns

Array of File

---

## Get File Path

Returns the path or URL of the input files.

Folder paths always end with a slash.

### Parameters

- **File** (Array of File)
- **Type** (`FilePathTypeAppEnum`)

### Returns

Array of Text

---

## Get High-Resolution Timestamp

Returns a timestamp representing the current instant in nanoseconds.

Example: 434055845120916

The most common use-case is to subtract two instances of this to get a highly accurate difference.

The timestamp is not meant to be stored for a long time. It's only unique for the current computer session.

### Returns

Number

---

## Get Image Capture Date

Returns the original capture date and time of the image from Exif metadata, if any.

See the “Set Image Capture Date” action for the inverse.

Related actions:
- Get Image Location

### Parameters

- **Image** (File)

### Returns

Date

---

## Get Image Location

Returns the capture location of the image from Exif metadata, if any.

The return value is in the format “-77.0364, 38.8951” (latitude, longitude).

See the “Set Image Location” action for the inverse.

Related actions:
- Get Image Capture Date

### Parameters

- **Image** (File)

### Returns

Text

---

## Get Index of List Item

Returns the position of the item in the list, or -1 if the item is not in the list.

It uses 1-based indexing.

### Parameters

- **List** (Array of Text)
- **Item** (Text)

### Returns

Number

---

## Get Map Image of Location

Returns an image with the given location marked and centered on a map.

On iOS & visionOS, it has to momentarily open the Actions app because the map image can only be generated by a foreground app. Afterwards, it goes back to the Shortcuts app. If you were running the shortcut in the background, there is unfortunately no way to go back to the previous app you were in, other than opening the app again from the shortcut.

### Parameters

- **Location** (Location)
- **Visible Radius** (Measurement of UnitLength)
- **Width** (Number)
- **Height** (Number)
- **Show Placemark** (Boolean)
- **Map Type** (`MapTypeAppEnum`)
- **Appearance** (`AppearanceAppEnum`)

### Returns

File

---

## Get Modifier Key State

Returns which modifier keys are currently pressed.

This can be useful to have alternative behavior when, for example, the user presses the Option key.

Supported modifier keys:
- Shift
- Control
- Option
- Command
- Function

### Returns

`ModifierKeyState_AppEntity`

---

## Get Music Playlists

Returns the names of the playlists in your Music library.

See the “Find Music Playlist” action for more advanced functionality.

### Returns

Array of Text

---

## Get Paragraphs from Text

Returns the text split into paragraphs.

Related action: Get Sentences from Text

### Parameters

- **Text** (Text)
- **Language** (`NLLanguageAppEntity`)

### Returns

Array of Text

---

## Get Query Item Value from URL

Returns the value of the first query item with the given name from the input URL.

### Parameters

- **URL** (URL)
- **Name** (Text)

### Returns

Text

---

## Get Query Items from URL

Returns all query items from the input URL.

The name and value of the query item can be accessed individually.

### Parameters

- **URL** (URL)

### Returns

Array of `URLQueryItemAppEntity`

---

## Get Query Items from URL as Dictionary

Returns all query items from the input URL as a dictionary.

This makes it convenient to get specific items.

Limitation: URLs support having multiple query items with the same name, but dictionaries cannot have duplicate keys.

Tip: You could, for example, use this action together with the built-in “Get Dictionary Value” action.

### Parameters

- **URL** (URL)

### Returns

File

---

## Get Random Boolean

Returns a random boolean. Think of it as a random “Yes” or “No” answer.

### Returns

Boolean

---

## Get Random Color

Returns a random color.

### Returns

`ColorAppEntity`

---

## Get Random Date and Time

Returns a random date and time in the given range.

### Parameters

- **Start** (Date)
- **End** (Date)

### Returns

Date

---

## Get Random Emoticon

Returns a random emoticon (also known as smiley).

### Returns

Text

---

## Get Random Floating-Point Number

Returns a random floating-point number between the given minimum and maximum value.

### Parameters

- **Minimum** (Double)
- **Maximum** (Double)
- **Seed** (Text)

### Returns

Double

---

## Get Random Number from Seed

Returns a random number between the given minimum and maximum value.

### Parameters

- **Minimum** (Number)
- **Maximum** (Number)
- **Seed** (Text)

### Returns

Number

---

## Get Related Words

Returns words related to the input word.

For example, given the word “horse”, it would return stallion, racehorse, pony, etc.

### Parameters

- **Word** (Text)
- **Maximum Count** (Number)
- **Language** (`NLLanguageAppEntity`)

### Returns

Array of Text

---

## Get Running Apps

IMPORTANT: Prefer the built-in “Find Apps” action. This one will be deprecated at some point.

Returns the currently running apps, including various metadata about them.

Use the built-in “Show Result” action to inspect the individual properties.

### Returns

Array of `RunningAppAppEntity`

---

## Get SF Symbol Image

Returns a SF Symbols symbol as an image.

For example, “checkmark.circle.fill”.

Use the SF Symbols app to find the symbol you want.

### Parameters

- **Symbol Name** (Text)
- **Size** (Number)
- **Rendering** (`SymbolImageRenderingAppEnum`)
- **Hex Color** (Text)
- **Hex Color** (Array of Text)
- **Weight** (`SymbolWeightAppEnum`)

### Returns

File

---

## Get Sentences from Text

Returns the text split into sentences.

Related action: Get Paragraphs from Text

### Parameters

- **Text** (Text)
- **Language** (`NLLanguageAppEntity`)

### Returns

Array of Text

---

## Get Title of URL

Returns the title of the given website, or nothing if it failed to get the title.

### Parameters

- **URL** (URL)

### Returns

Text

---

## Get Uniform Type Identifier

Returns the Uniform Type Identifier (UTI) of the input file.

For example, a JPEG file would return “public.jpeg”.


Related actions:
- Set Uniform Type Identifier
- Is Conforming to Uniform Type Identifier

### Parameters

- **File** (File)

### Returns

Text

---

## Get User Details

Returns details about the current user.

For example, username, name, language, idle time, etc.

### Parameters

- **Type** (`UserDetailsTypeAppEnum`)

### Returns

Text

---

## Get Values Using JSONPath

Returns values from a dictionary or JSON file using a JSONPath expression.

Tip: To pass in a dictionary, long-tap (iOS) or right-click (macOS) the “JSON File” parameter and select a variable to a dictionary.


EXAMPLE

Input:  {"users":[{"name":"John","age":30},{"name":"Jane","age":25}]}
Path:   $.users[*].name
Result: John, Jane

### Parameters

- **JSON File** (File)
- **JSONPath** (Text)

### Returns

Array of Text

---

## Global Variable: Delete

Delete global variables.

### Parameters

- **Delete All?** (Boolean)
- **Variables** (Array of Text)

---

## Global Variable: Get All

Returns all the global variables as a dictionary.

Tip: Use the built-in “Get Dictionary Value” action to access all keys.

### Returns

File

---

## Global Variable: Get Boolean

Returns the global variable with the given key if any.

### Parameters

- **Key** (Text)

### Returns

Boolean

---

## Global Variable: Get Number

Returns the global variable with the given key if any.

### Parameters

- **Key** (Text)

### Returns

Double

---

## Global Variable: Get Text

Returns the global variable with the given key if any.

### Parameters

- **Key** (Text)

### Returns

Text

---

## Global Variable: Set Boolean

Sets a global variable with the given boolean.

You can also toggle a boolean.

Global variables persist across your shortcuts and devices, with a limit of 1000 variables and a total storage capacity of 1 MB. Avoid using this for large amounts of data. For large data, use iCloud Drive, Notes, or Data Jar.

### Parameters

- **Action** (Boolean)
- **Key** (Text)
- **Value** (Boolean)

---

## Global Variable: Set Number

Sets a global variable with the given number.

You can also increment or decrement a number.

Global variables persist across your shortcuts and devices, with a limit of 1000 variables and a total storage capacity of 1 MB. Avoid using this for large amounts of data. For large data, use iCloud Drive, Notes, or Data Jar.

### Parameters

- **Action** (`GlobalVariableSetNumberAction_AppEnum`)
- **Key** (Text)
- **Value** (Double)

---

## Global Variable: Set Text

Sets a global variable with the given text.

Tip: You can store a dictionary of string/boolean/number values by passing it in as a variable. To get the persisted dictionary back, pass the output of the “Global Variables: Get Text” action to the “Get Dictionary from Input” action.

Global variables persist across your shortcuts and devices, with a limit of 1000 variables and a total storage capacity of 1 MB. Avoid using this for large amounts of data. For large data, use iCloud Drive, Notes, or Data Jar.

### Parameters

- **Key** (Text)
- **Value** (Text)

---

## Hex Encode

Encodes or decodes text or files using Hex encoding.

Example: Hi → 4869

Note: Use Base64 encoding whenever possible as it's more space efficient.

### Parameters

- **Input** (File)
- **Action** (`HexEncodeActionAppEnum`)
- **Uniform Type Identifier** (Text)

### Returns

File

---

## Hide Shortcuts App

Hides the Shortcuts app.

This is useful for making cross-platform shortcuts. If you just target iOS, use the built-in “Go to Home Screen” action instead.

---

## Invert Images

Invert the colors of the input images.

### Parameters

- **Images** (Array of File)

### Returns

Array of File

---

## Is Accessibility Feature On

Returns whether a certain accessibility feature is enabled.

On macOS, only the following are available. The rest always return false.
- Reduce Motion
- Reduce Transparency
- Invert Colors
- Increase Contrast
- Differentiate without Color
- VoiceOver
- Switch Control

It's unfortunately not possible to check for “Assistive Touch”, “Guided Access”, or anything else. This action exposes what Apple provides for checks.

### Parameters

- **Feature** (`AccessibilityFeature_AppEnum`)

### Returns

Boolean

---

## Is Audio Playing

Returns whether there is audio currently playing on the device.

Important: The action simply returns the value that the system provides, so if there are any false-positives, there is unfortunately not much we can do about it. I recommend trying to restart your device, which sometimes fixes such issues.

Known issues
- It incorrectly returns “true” if the microphone is active.
- It incorrectly returns “true” if you have the “Accessibility › Sound Recognition” system setting enabled.
- It returns “false” if audio is playing through AirPlay. There is unfortunately no way to detect this.
- It returns “true” for a while after you end a call, even though no audio is playing.

### Returns

Boolean

---

## Is Bluetooth On

Returns whether Bluetooth is on or off.

NOTE: You need to allow the Bluetooth permission in the main app before using this action.

### Returns

Boolean

---

## Is Call Active

Returns whether the device is on a call (phone, FaceTime, VoIP, etc).

On macOS, it always returns “false”.

### Returns

Boolean

---

## Is Camera On

Returns whether any camera on the computer is on.

### Returns

Boolean

---

## Is Cellular Data On

Returns whether cellular data is enabled on the device.

On macOS and visionOS, it always returns false.

### Returns

Boolean

---

## Is Cellular Low Data Mode On

Returns whether cellular low data mode is enabled on the device.

On macOS and visionOS, it always returns false.

### Returns

Boolean

---

## Is Conforming to Uniform Type Identifier

Returns whether the given Uniform Type Identifier (UTI) conforms to another one.

For example, it would return true if the first parameter is “public.jpeg” (JPEG image) and the second parameter is “public.image”.

This could be useful in combination with the “Get Uniform Type Identifier” action to check if a file conforms to a certain UTI. For example, to check if a file is an image.

### Parameters

- **UTI** (Text)
- **Parent UTI** (Text)

### Returns

Boolean

---

## Is Connected to VPN

Returns whether the device is connected to a VPN.

Note: There are some VPN protocols it is not able to detect. If the check is not working, try selecting a different VPN protocol in your VPN provider's app if possible. For example, the WireGuard protocol is known to not be detectable, while OpenVPN, IKEv2, and IPSec are detectable.

### Returns

Boolean

---

## Is Dark Mode On

Returns whether dark mode is enabled on the device.

NOTE: This always returns "“false” on visionOS.

### Returns

Boolean

---

## Is Day

Checks if the input date corresponds to a specific weekday, today, tomorrow, yesterday, or falls on a weekend.

### Parameters

- **Day** (Date)
- **Type** (`DayType_AppEnum`)

### Returns

Boolean

---

## Is Device Locked

Returns whether the device is currently locked.

Limitations:
- It takes about 10 seconds from when you lock the screen until the device is actually locked.
- This will not work if you don't have any authentication (passcode, Face ID, or Touch ID) for the device.

### Returns

Boolean

---

## Is Device Moving

Returns whether the device is currently moving.

If no movement is detect within 1 second, it returns “false”.

This can be useful to detect whether the device is in use or not.

NOTE: On macOS and visionOS, it always returns “false”.

### Parameters

- **Timeout (seconds)** (Double)
- **Minimum Acceleration** (Double)

### Returns

Boolean

---

## Is Device Orientation

Returns whether the device is in the chosen orientation.

On macOS and visionOS, it always returns “false”.

### Parameters

- **Orientation** (`IsDeviceOrientationAppEnum`)

### Returns

Boolean

---

## Is Host Reachable

Returns whether the host at the given domain or IP address is reachable.

Use the “Is Web Server Reachable” action if the host is a web server.

### Parameters

- **Host** (Text)
- **Port** (Number)
- **Timeout (seconds)** (Double)
- **Debug** (Boolean)

### Returns

Boolean

---

## Is Low Power Mode On

Returns whether low power mode is enabled on the device.

### Returns

Boolean

---

## Is Microphone On

Returns whether any microphone on the computer is on.

### Returns

Boolean

---

## Is Online

Returns whether the computer is online. It tries to connect to one or more servers to ensure you're actually online.

### Returns

Boolean

---

## Is Screen Locked

Returns whether the screen is locked.

### Returns

Boolean

---

## Is Shaking Device

Returns whether you are currently shaking the device.

If no shaking is detect within 2 seconds, it returns “false”.

On macOS and visionOS, it always returns “false”.

### Parameters

- **Timeout (seconds)** (Double)

### Returns

Boolean

---

## Is Silent Mode On

Returns whether the silent switch (mute) is enabled on the device.

Known limitation: This will return true even if silent mode is not enabled if it's run while Voice Memos is recording.

### Returns

Boolean

---

## Is Time

Checks if the input time corresponds to the current hour and minute.

### Parameters

- **Time** (Date)

### Returns

Boolean

---

## Is Time In Range

Checks if a given time (or current time if not specified) falls within a specified time range.

It only uses the times from the given dates.

It correctly handles overnight/reverse ranges (e.g. 14:00 to 11:00).

### Parameters

- **Target Time** (Date)
- **Start Time** (Date)
- **End Time** (Date)

### Returns

Boolean

---

## Is Web Server Reachable

Returns whether the web server at the given host or URL is reachable.

Use the “Is Online” action if you just want to check whether your computer is online.

Use the “Is Host Reachable” action if you want to check reachability with a host that is not a web server.

### Parameters

- **Host** (Text)
- **Timeout (seconds)** (Double)
- **Require success (2xx) status code** (Boolean)
- **Use GET instead of HEAD** (Boolean)

### Returns

Boolean

---

## Is Wi-Fi On

Returns whether Wi-Fi is turned on.

It returns false if the device does not support Wi-Fi.

Use the “Is Online” action if you simply want to check for internet connectivity.

### Returns

Boolean

---

## Join Wi-Fi

Joins the given Wi-Fi network.

NOTE: It is not possible to join a Wi-Fi network without the join prompt.

NOTE: The prompt to join a Wi-Fi network can only be presented in an app, so the action has to open the Actions app momentarily and then it switches back to the Shortcuts app. If you're running the shortcut in the background, you may want to add the “Go to Home Screen” action after this one.

FAQ: Can you add the inverse, a way to disconnect Wi-Fi? That is not possible.

### Parameters

- **Name (SSID)** (Text)
- **Password** (Text)
- **Wait for Connection** (Boolean)
- **Is WEP** (Boolean)
- **Is Hidden** (Boolean)

---

## Merge Dictionaries

Merges two or more dictionaries into one dictionary.

Supports up to 10 dictionaries.

It does shallow merging.

Tap and hold a dictionary parameter to select a variable to a dictionary. Don't quick tap it.

In Shortcuts, dictionaries are just JSON, so you can use this to merge JSON (file or text) too.


Implementation note: It uses 10 parameters instead of simply a list of dictionaries because the Shortcuts app crashes if the latter is used.

### Parameters

- **Dictionary 1** (File)
- **Dictionary 2** (File)
- **Dictionary 3** (File)
- **Dictionary 4** (File)
- **Dictionary 5** (File)
- **Dictionary 6** (File)
- **Dictionary 7** (File)
- **Dictionary 8** (File)
- **Dictionary 9** (File)
- **Dictionary 10** (File)

### Returns

File

---

## Named Clipboard: Clear

Clears a named clipboard.

A named clipboard is a semi-private clipboard only accessible if you know the name. It can be useful to share data between shortcuts without cluttering the main clipboard.

### Parameters

- **Name** (Text)

---

## Named Clipboard: Get Data

Returns one or more items from a named clipboard.

A named clipboard is a semi-private clipboard only accessible if you know the name. It can be useful to share data between shortcuts without cluttering the main clipboard.

See the “Set Data from Named Clipboard” action to set items.
See the “Get Text from Named Clipboard” action to get text.

### Parameters

- **Name** (Text)
- **Type** (Text)

### Returns

Array of File

---

## Named Clipboard: Get Text

Returns one or more text items from a named clipboard.

A named clipboard is a semi-private clipboard only accessible if you know the name. It can be useful to share data between shortcuts without cluttering the main clipboard.

See the “Set Text from Named Clipboard” action to set items.
See the “Get Data from Named Clipboard” action to get other things like images.

### Parameters

- **Name** (Text)

### Returns

Array of Text

---

## Named Clipboard: Set Data

Sets one or more items on a named clipboard.

A named clipboard is a semi-private clipboard only accessible if you know the name. It can be useful to share data between shortcuts without cluttering the main clipboard.

See the “Get Data from Named Clipboard” action to get items.
See the “Set Text from Named Clipboard” action to set text.

### Parameters

- **Name** (Text)
- **Items** (Array of File)

---

## Named Clipboard: Set Text

Sets one or more text items on a named clipboard.

A named clipboard is a semi-private clipboard only accessible if you know the name. It can be useful to share data between shortcuts without cluttering the main clipboard.

See the “Get Text from Named Clipboard” action to get items.
See the “Set Data from Named Clipboard” action to set other things like images.

### Parameters

- **Name** (Text)
- **Text Items** (Array of Text)

---

## Open URLs in Safari

Helps you open the specified URLs in Safari.

IMPORTANT: You need to pass the result of this action to the built-in “Open URLs” action.

It only supports HTTPS and HTTP URLs.

This is different from the built-in “Open URLs” action which opens the URL in the default browser (even though its action description says it opens in Safari only).

On macOS, you can alternatively use the “Open URLs with App” to open URLs in any browser.

### Parameters

- **URLs** (Array of URL)

### Returns

Array of URL

---

## Open URLs with App

Opens URLs in a specific app.

This only works for apps that declare they can open URLs. Click the app parameter to see those apps.

Tip: Check out the action that comes with my Velja app if you need to open URLs with an app that does not declare support for URLs.

### Parameters

- **URL** (Array of URL)
- **App** (`App_AppEntity`)
- **Open in background** (Boolean)
- **Hide other apps** (Boolean)

---

## Overwrite File

Overwrites the given destination file with the given source file.

Returns the new destination file.

### Parameters

- **Source** (File)
- **Destination** (File)

### Returns

File

---

## Parse CSV

Parses CSV into a list of dictionaries.

### Parameters

- **CSV** (File)
- **First Row Is Header** (Boolean)
- **Delimiter** (`CSVDelimiterAppEnum`)
- **Custom Delimiter** (Text)

### Returns

Array of File

---

## Parse JSON5

Parses JSON5 into a dictionary.

JSON5 is a more human-friendly version of JSON. It can handle comments, single-quotes, and more.

The built-in “Get Dictionary from Input” action does not support JSON5.

### Parameters

- **JSON5** (File)

### Returns

File

---

## Pick Color

Lets you pick a color using the system color picker.

Optionally pick a color from an image.

NOTE: On iOS, you need to pick a color within 25 seconds, otherwise the action times out (iOS limitation).

### Parameters

- **Initial Color** (`ColorAppEntity`)
- **Reference Image** (File)

### Returns

`ColorAppEntity`

---

## Play Alert Sound

Plays the user preferred alert sound.

---

## Pretty Print Dictionaries

Formats dictionaries (JSON) to be prettier and more readable.

### Parameters

- **Dictionary** (Array of Text)

### Returns

Array of Text

---

## Remove Duplicate Lines

Removes duplicate lines from the input text. Empty or whitespace-only lines are not considered duplicates.

### Parameters

- **Text** (Text)
- **Case Insensitive** (Boolean)

### Returns

Text

---

## Remove Duplicates from List

Removes duplicates from the input list.

Note: If you get the error “The operation failed because Shortcuts couldn't convert from Text to NSString.”, just change the preview to show a list view instead. This is a bug in the Shortcuts app.

### Parameters

- **List** (Array of File)

### Returns

Array of File

---

## Remove Emojis

Removes all emojis in the input text.

### Parameters

- **Text** (Text)

### Returns

Text

---

## Remove Empty Lines

Removes empty and whitespace-only lines from the input text.

### Parameters

- **Text** (Text)

### Returns

Text

---

## Remove Non-Printable Characters

Removes non-printable (invisible) Unicode characters from the input text, excluding normal whitespace characters.

This can be useful to clean up input text which might contain things like left-to-right embedding, control characters, etc.

### Parameters

- **Text** (Text)

### Returns

Text

---

## Remove Notifications

Removes either specific, all, pending, or delivered notifications created by the "Show Notification” action.

### Parameters

- **Action** (`RemoveNotificationsAction`)
- **Notifications** (Array of `Notification_AppEntity`)

---

## Remove from List

Removes items from the input list.

It uses 1-based indexing.

Note: If you get the error “The operation failed because Shortcuts couldn't convert from Text to NSString.”, just change the preview to show a list view instead. This is a bug in the Shortcuts app.

### Parameters

- **List** (Array of File)
- **Action** (`RemoveFromListActionAppEnum`)
- **Index** (Number)
- **Start Index** (Number)
- **End Index** (Number)
- **Count** (Number)

### Returns

Array of File

---

## Reverse Lines

Reverses the lines of the input text.

### Parameters

- **Text** (Text)

### Returns

Text

---

## Reverse List

Reverses the input list.

Note: If you get the error “The operation failed because Shortcuts couldn't convert from Text to NSString.”, just change the preview to show a list view instead. This is a bug in the Shortcuts app.

### Parameters

- **List** (Array of File)

### Returns

Array of File

---

## Round Number to Multiple

Rounds the input number to the nearest multiple of the second number.

For example, if the number represents minutes and you want to round it to the nearest half-hour, you could use 30 as the multiple.

### Parameters

- **Number** (Double)
- **Multiple** (Number)
- **Mode** (`NumberRoundingModeAppEnum`)

### Returns

Number

---

## Sample Color from Screen

Lets you pick a color from the screen.

### Returns

`ColorAppEntity`

---

## Scan Documents

Scans one or more documents using the system document scanner.

IMPORTANT: The resulting images are copied to the clipboard. Add the “Wait to Return” and “Get Clipboard” actions after this one.

NOTE: In contrast to the built-in “Scan Document” action, this one makes it possible to use the scanned document in the shortcut.

### Parameters

- **Use PDF** (Boolean)

---

## Scan QR Codes in Image

Returns the messages of the QR codes in the input image.

By default, it only returns the message for the first QR code.

The messages are sorted by the physical size of their QR code in ascending order (largest first).

### Parameters

- **Image** (File)
- **Scan Multiple** (Boolean)

### Returns

Array of Text

---

## Send Feedback

Lets you send feedback, action ideas, bug reports, etc, directly to the developer of the Actions app. You can also email me at sindresorhus@gmail.com if you prefer that.

### Parameters

- **Message** (Text)
- **Your Email** (Text)

### Returns

Text

---

## Set Creation and Modification Date of File

Sets the creation and modification date of a file or folder to a new value.

To be able to select a folder, use the built-in “Folder” action.

Note: Setting the modification date of a file/folder in iCloud may not work as iCloud changes the modification date when it syncs.

Related actions:
- Set Image Capture Date

### Parameters

- **File** (File)
- **Type** (`SetFileDateTypeAppEnum`)
- **Date and Time** (Date)
- **Modify Original** (Boolean)

### Returns

File

---

## Set Default Printer

Sets the default printer.

### Parameters

- **Printer** (`PrinterAppEntity`)

---

## Set Image Capture Date

Sets the capture date and time (Exif metadata) of the input images.

Note: It only modifies the image in the workflow, not the original image.

See the “Get Image Capture Date” action for the inverse.

Related actions:
- Set Image Location
- Set Creation and Modification Date of File

### Parameters

- **Capture Date and Time** (Date)
- **Images** (Array of File)

### Returns

Array of File

---

## Set Image Location

Sets the capture location (Exif metadata) of the input images.

Note: It only modifies the image in the workflow, not the original image.

See the “Get Image Location” action for the inverse.

Related actions:
- Set Image Capture Date

### Parameters

- **Latitude & Longitude** (Text)
- **Image** (Array of File)

### Returns

Array of File

---

## Set Uniform Type Identifier

Sets the Uniform Type Identifier (UTI) of the input files.

This can be useful when the previous shortcut action returned some data without a specific type.

### Parameters

- **Files** (Array of File)
- **Type Identifier** (Text)

### Returns

Array of File

---

## Show Notification

Displays a system notification.

Returns the notification.

Use the “Find Notification” action to list pending and delivered notifications.

Use the “Remove Notifications” action to remove one or more notifications.

FAQ: Can it support more advanced repeat patterns or multiple triggers? No, notifications do not support that. You can instead schedule multiple notifications. You could also use Shortcuts automations to schedule notifications.

Note: The system allows up to 64 scheduled notifications at a time from this action. When exceeded, the system automatically removes the oldest scheduled notifications to accommodate new ones.

### Parameters

- **Title** (Text)
- **Subtitle** (Text)
- **Body** (Text)
- **Attachment** (File)
- **When** (`NotificationTiming_AppEnum`)
- **Show at Time** (Date)
- **Show after Duration** (Measurement of UnitDuration)
- **Location** (Location)
- **Location Radius** (Double)
- **Repeats** (Boolean)
- **Is Time Sensitive** (Boolean)
- **Identifier** (Text)
- **Thread Identifier** (Text)
- **Sound** (`NotificationSound_AppEnum`)
- **Custom Sound** (File)
- **Open URL on Tap** (URL)
- **Actions** (Array of `NotificationAction_AppEntity`)
- **Data** (Text)

### Returns

`Notification_AppEntity`

---

## Shuffle List

Shuffles the input list.

Note: If you get the error “The operation failed because Shortcuts couldn't convert from Text to NSString.”, just change the preview to show a list view instead. This is a bug in the Shortcuts app.

### Parameters

- **List** (Array of File)
- **Limit** (Boolean)
- **Maximum Results** (Number)

### Returns

Array of File

---

## Sort List

Sorts the input list.

Note: If you get the error “The operation failed because Shortcuts couldn't convert from Text to NSString.”, just change the preview to show a list view instead. This is a bug in the Shortcuts app.

Note: The number sort type expects a list of just numbers, not strings with both text and numbers in them.

Tip: Use the natural sort type to correctly sort things like filenames (for example, `011 Foo` and `006 Bar`).

### Parameters

- **List** (Array of Text)
- **Sort Order** (Boolean)
- **Sort Type** (`SortTypeAppEnum`)

### Returns

Array of Text

---

## Sort Months

Sorts a list of month names based on their chronological order.

Supports both full and abbreviated month names. For example, “January” and "Jan".

### Parameters

- **Months** (Array of Text)
- **Sort Order** (Boolean)
- **Locale** (`LocaleAppEntity`)

### Returns

Array of Text

---

## Spell Out Number

Spells out the input number.

For example, 1000 becomes “one thousand”.

If a locale is not specified, the system locale is used.

### Parameters

- **Number** (Number)
- **Locale** (`LocaleAppEntity`)

### Returns

Text

---

## Toggle Boolean

Inverts the given boolean value. If the input is true, the output will be false, and vice versa.

It can be useful together with the “If” action when checking multiple conditions, but one of them needs to be inverted.

### Parameters

- **Boolean** (Boolean)

### Returns

Boolean

---

## Transcribe Audio (Legacy)

Converts the speech in the input audio file to text.

Note: Prefer the built-in “Transcribe Audio” action. This action will be deprecated at some point.

Note: On iOS & visionOS, the transcription only works if the audio takes less than 30 seconds to process. This usually means about 1 minute of transcription. This is because third-party actions only get 30 seconds to execute.

Tip: Check out my app Aiko on the App Store. It has higher quality transcription, unlimited duration, and supports 100 languages.

See the built-in “Dictate Text” action if you need to transcribe in real-time.

Important: If you have permission issues even after granting access, try removing the action from your shortcut, force quit Shortcuts and Actions, and then add the action again.

### Parameters

- **Audio File** (File)
- **Custom Locale (Many of the locales do not work because of a system bug)** (`SFLocaleAppEntity`)
- **Perform Offline (Buggy, don't use)** (Boolean)

### Returns

Text

---

## Transform Lists

Transforms items of two lists.

Note that duplicates will be removed from the result.

Tap and hold a list parameter to select a variable to a list. Don't quick tap it.

Note: If you get the error “The operation failed because Shortcuts couldn't convert from Text to NSString.”, just change the preview to show a list view instead. This is a bug in the Shortcuts app.

Known limitation: It does not work with iTunes Media items.

### Parameters

- **Operation** (`OperationTypeAppEnum`)
- **List 1** (Array of File)
- **List 2** (Array of File)

### Returns

Array of File

---

## Transform Text

Transforms the input text to camel case, pascal case, snake case, constant case, or dash case. It also has transliteration transformations.

### Parameters

- **Text** (Text)
- **Transformation** (`TransformationAppEnum`)

### Returns

Text

---

## Transform Text with JavaScript

Transforms the input text with the given JavaScript code.

The input text is available in a global variable named “$text”.

The code is excuted with JavaScriptCore (same as used in Safari), not JXA.

### Parameters

- **Text** (Text)
- **JavaScript Code** (Text)

### Returns

Text

---

## Trim Whitespace

Removes leading & trailing whitespace and newline characters from the input text.

### Parameters

- **Text** (Text)

### Returns

Text

---

## Truncate List

Truncates the input list to the given limit by removing items from the end.

Note: If you get the error “The operation failed because Shortcuts couldn't convert from Text to NSString.”, just change the preview to show a list view instead. This is a bug in the Shortcuts app.

### Parameters

- **List** (Array of File)
- **Count** (Number)

### Returns

Array of File

---

## Truncate Number

Removes the fractional part of the given number.

Example: 3.4 => 3
Example: 3.457 => 3.45

### Parameters

- **Number** (Double)
- **Decimal Places** (Number)

### Returns

Double

---

## Truncate Text

Truncates the input text from the end to the given maximum length.

### Parameters

- **Text** (Text)
- **Maximum Length** (Number)
- **Truncation Indicator** (Text)

### Returns

Text

---

## Wait Milliseconds

Waits for the specified number of milliseconds before continuing with the next action.

It is guaranteed to take at least the given amount of milliseconds. Sometimes it may take slightly longer.

Use the built-in “Wait” action for durations longer than 1 second.

### Parameters

- **Duration** (Number)

---

## Write or Edit Text

Opens a text editor where you can write or edit text.

IMPORTANT: The result is copied to the clipboard. Add the “Wait to Return” and “Get Clipboard” actions after this one.

### Parameters

- **Text** (Text)
- **Edit** (Boolean)
- **Editor Title** (Text)

---


