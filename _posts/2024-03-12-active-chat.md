---
categories:
  - GPT
tags:
  - AI
comment: 'https://raw.githubusercontent.com/OvidijusParsiunas/active-chat/main/website/docs/docs/speech.mdx'
info: aberto.
date: '2024-03-12'
type: post
layout: post
published: true
slug: active-chat
title: 'Active Chat Speech'
mermaid: true
---

import azureCredentials from '/img/azure-credentials.png'; # Speech  \### \`textToSpeech\` {#textToSpeech} - Type: \`true\` | \\{  
     \`voiceName?: string\`,  
     \`lang?: string\`,  
     \`pitch?: number\`,  
     \`rate?: string\`,  
     \`volume?: number\`  
\\} When the chat receives a new text message - your device will automatically read it out.  
\`voiceName\` is the name of the voice that will be used to read out the incoming message. Please note that different Operating Systems support different voices. Use the following code snippet to see the available voices for your device: \`window.speechSynthesis.getVoices()\`  
\`lang\` is used to set the utterance language. See the following \[\`QA\`\](https://stackoverflow.com/questions/23733537/what-are-the-supported-languages-for-web-speech-api-in-html5) for the available options.  
\`pitch\` sets the pitch at which the utterance will be spoken at.  
\`volume\` set the volume at which the utterance will be spoken at. :::info Text to speech is using \[\`SpeechSynthesis\`\](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis) Web API which is supported differently across different devices. ::: :::info Your mouse needs to be focused on the browser window for this to work. ::: import ComponentContainer from '@site/src/components/chat/componentContainer'; import DeepChatBrowser from '@site/src/components/chat/deepChatBrowser'; import LineBreak from '@site/src/components/markdown/lineBreak'; import BrowserOnly from '@docusaurus/BrowserOnly'; import TabItem from '@theme/TabItem'; import Tabs from '@theme/Tabs'; {() => require('@site/src/components/nav/autoNavToggle').readdAutoNavShadowToggle()} {() => require('@site/src/components/externalModules/speechToElement').checkWebSpeechSupport()} #### Example \`\`\`html \`\`\` \`\`\`html \`\`\` \### \`speechToText\` {#speechToText} - Type: \`true\` | \\{  
     \`webSpeech?:\` \`true\` | \[\`WebSpeechOptions\`\](#WebSpeechOptions),  
     \[\`azure?: AzureOptions\`\](#AzureOptions),  
     \[\`textColor?: TextColor\`\](#TextColor),  
     \`displayInterimResults?: boolean\`,  
     \`translations?: {\[key: string\]: string}\`,  
     \[\`commands?: Commands\`\](#Commands),  
     \[\`button?: ButtonStyles\`\](#ButtonStyles),  
     \`stopAfterSubmit?: boolean\`,  
     \[\`submitAfterSilence?: SubmitAfterSilence\`\](#SubmitAfterSilence)  
\\} - Default: \_\\{webSpeech: true, stopAfterSubmit: true\\}\_ Transcribe your voice into text and control chat with commands.  
\`webSpeech\` utilises \[\`Web Speech API\`\](https://developer.mozilla.org/en-US/docs/Web/API/Web\_Speech\_API/Using\_the\_Web\_Speech\_API) to transcribe your speech.  
\`azure\` utilises \[\`Azure Cognitive Speech Services API\`\](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-to-text) to transcribe your speech.  
\`textColor\` is used to set the color of interim and final results text.  
\`displayInterimResults\` controls whether interim results are displayed.  
\`translations\` is a case-sensitive one-to-one mapping of words that will automatically be translated to others.  
\`commands\` is used to set the phrases that will trigger various chat functionality.  
\`button\` defines the styling used for the microphone button.  
\`stopAfterSubmit\` is used to toggle whether the recording stops after a message has been submitted.  
\`submitAfterSilence\` configures automated message submit functionality when the user stops speaking.  

[Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API) is not supported in this browser.

\#### Example \`\`\`html \`\`\` \`\`\`html \`\`\` :::info If the \[\`microphone\`\](/docs/files#microphone) recorder is set - this will not be enabled.  
::: :::info Speech to text functionality is provided by the \[\`Speech To Element\`\](https://github.com/OvidijusParsiunas/speech-to-element) library. ::: :::caution Support for \`webSpeech\` varies across different browsers, please check the \[\`Can I use\`\](https://caniuse.com/?search=Web%20Speech%20API) Speech Recognition API section. (The yellow bars indicate that it is supported) ::: \## Types Object types for \[\`speechToText\`\](#speechToText): ### \`WebSpeechOptions\` {#WebSpeechOptions} - Type: \\{\`language?: string\`\\} \`language\` is used to set the recognition language. See the following \[\`QA\`\](https://stackoverflow.com/questions/23733537/what-are-the-supported-languages-for-web-speech-api-in-html5) for the full list.

[Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API) is not supported in this browser.

\#### Example \`\`\`html \`\`\` \`\`\`html \`\`\` :::note This service stops after a brief period of silence due to limitations in its API and not Deep Chat. ::: \### \`AzureOptions\` {#AzureOptions} - Type: \\{  
     \`region: string\`,  
     \`retrieveToken?: () => Promise\`,  
     \`subscriptionKey?: string\`,  
     \`token?: string\`,  
     \`language?: string\`,  
     \`stopAfterSilenceMs?: number\`  
\\} - Default: \_\\{stopAfterSilenceMs: 25000 (25 seconds)\\}\_ This object requires \`region\` and either \`retrieveToken\`, \`subscriptionKey\` or the \`token\` properties to be defined with it:  
\`region\` is the location/region of your Azure speech resource.  
\`retrieveToken\` is a function used to retrieve a new token for the Azure speech resource. It is the recommended property to use as it can retrieve the token from a secure server that will hide your credentials. Check out the \[retrieval example\](#retrieve-token-example) below and \[starter server templates\](https://github.com/OvidijusParsiunas/speech-to-element/tree/main/examples).  
\`subscriptionKey\` is the subscription key for the Azure speech resource.  
\`token\` is a temporary token for the Azure speech resource.  
\`language\` is a BCP-47 string value to denote the recognition language. You can find the full list \[here\](https://docs.microsoft.com/azure/cognitive-services/speech-service/supported-languages).  
\`stopAfterSilenceMs\` is the milliseconds of silence required for the microphone to automatically turn off.  
:::info To use the Azure Speech To Text service - please add the \[\`Speech SDK\`\](https://www.npmjs.com/package/microsoft-cognitiveservices-speech-sdk) to your project. See \[EXAMPLES\](/examples/externalModules). ::: #### Example \`\`\`html \`\`\` \`\`\`html \`\`\` Location of speech service credentials in Azure Portal: ![]({azureCredentials}) :::caution The \`subscriptionKey\` and \`token\` properties should only be used for local/prototyping/demo purposes ONLY. When you are ready to deploy your application, please switch to using the \`retrieveToken\` property. Check out the example below and \[starter server templates\](https://github.com/OvidijusParsiunas/speech-to-element/tree/main/examples). ::: \#### Retrieve token example { return fetch('http://localhost:8080/token') .then((res) => res.text()) .then((token) => token) .catch((error) => console.error('error')); }, }, }} > \`\`\`javascript speechToText.speechToText = { region: 'resource-region', retrieveToken: async () => { return fetch('http://localhost:8080/token') .then((res) => res.text()) .then((token) => token); }, }; \`\`\` \### \`TextColor\` {#TextColor} - Type: \\{\`interim?: string\`, \`final?: string\`\\} This object is used to set the color of \`interim\` and \`final\` results text.  
\#### Example \`\`\`html \`\`\` \`\`\`html \`\`\` \### \`Commands\` {#Commands} - Type: \\{  
     \`stop?: string\`,  
     \`pause?: string\`,  
     \`resume?: string\`,  
     \`removeAllText?: string\`,  
     \`submit?: string\`,  
     \`commandMode?: string\`,  
     \`settings?:\` \\{\`substrings?: boolean\`, \`caseSensitive?: boolean\`\\}  
\\} - Default: \_\\{settings: \\{substrings: true, caseSensitive: false\\}\\}\_ This object is used to set the phrases which will control chat functionality via speech.  
\`stop\` is used to stop the speech service.  
\`pause\` will temporarily stop the transcription and will re-enable it after the phrase for \`resume\` is spoken.  
\`removeAllText\` is used to remove all input text.  
\`submit\` will send the current input text.  
\`commandMode\` is a phrase that is used to activate the command mode which will not transcribe any text and will wait for a command to be executed. To leave the command mode - you can use the phrase for the \`resume\` command.  
\`substrings\` is used to toggle whether command phrases can be part of spoken words or if they are whole words. E.g. when this is set to \_true\_ and your command phrase is \_"stop"\_ - when you say "stopping" the command will be executed. However if it is set to \_false\_ - the command will only be executed if you say "stop".  
\`caseSensitive\` is used to toggle if command phrases are case sensitive. E.g. if this is set to \_true\_ and your command phrase is \_"stop"\_ - when the service recognizes your speech as "Stop" it will not execute your command. On the other hand if it is set to \_false\_ it will execute. #### Example \`\`\`html \`\`\` \`\`\`html \`\`\` \### \`ButtonStyles\` {#ButtonStyles} - Type: \\{\[\`commandMode?: ButtonStyles\`\](/docs/styles/#ButtonStyles), \[\`MicrophoneStyles\`\](/docs/styles/#MicrophoneStyles)\\} This object is used to define the styling for the microphone button.  
It contains the same properties as the \[\`MicrophoneStyles\`\](/docs/styles/#MicrophoneStyles) object and an additional \`commandMode\` property which sets the button styling when the \[\`command mode\`\](#Commands) is activated.  
\#### Example \`\`\`html \`\`\` \`\`\`html \`\`\` :::tip You can use the \[\`CSSFilterConverter\`\](https://cssfilterconverter.com/) tool to generate filter values for the icon color. ::: \### \`SubmitAfterSilence\` {#SubmitAfterSilence} - Type: \`true\` | \`number\` Automatically submit the input message after a period of silence.  
This property accepts the value of \_true\_ or a number which represents the milliseconds of silence required to wait before a messaget is submitted. If this is set to \_true\_ the default milliseconds is \_2000\_.  
\#### Example \`\`\`html \`\`\` \`\`\`html \`\`\` :::caution When using the default \[\`Web Speech API\`\](https://developer.mozilla.org/en-US/docs/Web/API/Web\_Speech\_API/Using\_the\_Web\_Speech\_API) - the recording will automatically stop after 5-7 seconds of silence, please take care when setting the \`ms\` property. ::: \## Demo This is the example used in the \[demo video\](https://github.com/OvidijusParsiunas/deep-chat/assets/18709577/e103a42e-b3a7-4449-b9db-73fed6d7876e). When replicating - make sure to add the Speech SDK to your project and add your resource properties. \`\`\`html

\`\`\`
