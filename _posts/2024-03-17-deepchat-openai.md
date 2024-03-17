---
categories:
  - GPT
tags:
  - AI
comment: https://github.com/OvidijusParsiunas/deep-chat/issues/53
info: aberto.
date: '2024-03-17'
type: post
layout: post
published: true
slug: deepchat-openai
title: 'Deep Chat OpenAI'
mermaid: true
---


### 
**[7h360df47h3r](/7h360df47h3r)** commented [Nov 27, 2023](#issue-2012537925)
### Feature Request: Support Passing Assistant Details in Custom Requests
**Current Behavior:**  
I am utilising your deep-chat-nextjs server as a proxy for OpenAI and the `request` prop in the `DeepChat` component does not support assistant parameters like the Direct Connection for OpenAI.
**Desired Behavior:**  
I would like to request support for passing assistant details in the `request` prop.
**Additional Information**  
If an update is not feasible, it would be greatly appreciated if you could provide guidance on how to achieve the requested functionality manually using custom headers and what it would look like on the nextjs example server.
The text was updated successfully, but these errors were encountered:
  
  
[![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](/OvidijusParsiunas) [OvidijusParsiunas](/OvidijusParsiunas) self-assigned this [Nov 27, 2023](#event-11073246256)
[![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](/OvidijusParsiunas) [OvidijusParsiunas](/OvidijusParsiunas) added the [advice](/OvidijusParsiunas/deep-chat/labels/advice) Information how to use/implement the component label [Nov 27, 2023](#event-11073246617)
Owner
### 
**[OvidijusParsiunas](/OvidijusParsiunas)** commented [Nov 27, 2023](#issuecomment-1828381507)
Hi. When connecting Deep Chat to your own backend (like a NextJs function), the specific code for calling another service such as [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview) should be written in the backend and not in Deep Chat.
We try to keep the backend examples as simple as possible so that developers can tailor them to their use-cases, hence we would prefer not to expand our examples for this reason.
In regards to your specific problem, connecting to [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview) is a quite complex task as it requires the use of the [Assistants](https://platform.openai.com/docs/api-reference/assistants), [Threads](https://platform.openai.com/docs/api-reference/threads), [Messages](https://platform.openai.com/docs/api-reference/messages) and [Runs](https://platform.openai.com/docs/api-reference/runs) APIs.
If you want to do this manually in your own backend, you can use the code that I will paste below.
  
  
 ![+1](https://github.githubassets.com/assets/1f44d-41cb66fe1e22.png) 2 7h360df47h3r and myfypersonal reacted with thumbs up emoji
-   ![+1](https://github.githubassets.com/assets/1f44d-41cb66fe1e22.png) 2 reactions
Owner
### 
**[OvidijusParsiunas](/OvidijusParsiunas)** commented [Nov 27, 2023](#issuecomment-1828383196) •
edited
Code for the [`index.tsx`](https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/nextjs/pages/index.tsx) file:
```
import {RequestDetails} from 'deep-chat/dist/types/interceptors';
import {Response} from 'deep-chat/dist/types/response';
import styles from '../styles/Index.module.css';
import dynamic from 'next/dynamic';
import React from 'react';
export default function IndexPage() {
  // Need to import the component dynamically as it uses the 'window' property.
  // If you have found a better way of adding the component in next, please create a new issue ticket so we can update the example!
  const DeepChat = dynamic(() => import('deep-chat-react').then((mod) => mod.DeepChat), {
    ssr: false,
  });
  // quick way to store state and not re-render the chat
  const threadId = React.useRef<string | null>('');
  return (
    <>
      <main className={styles.main}>
        <h1 className={styles.serverTitle}>Server for OpenAI</h1>
        <a href="https://openai.com/blog/openai-api" target="_blank" rel="noreferrer">
          <img
            className={styles.serverTitleIcon}
            src="https://raw.githubusercontent.com/OvidijusParsiunas/deep-chat/HEAD/website/static/img/openAILogo.png"
            style={{width: 26, marginBottom: '-1px'}}
            alt={'Title icon'}
          />
        </a>
        <h3>Make sure to set the OPENAI_API_KEY environment variable in your server</h3>
        <div className={styles.components}>
          <div className={styles.diagonalLine} style={{background: '#f2f2f2'}}></div>
          {/* by setting maxMessages requestBodyLimits to 0 or lower - each request will send full chat history:
            https://deepchat.dev/docs/connect/#requestBodyLimits */}
          <DeepChat
            style={{borderRadius: '10px'}}
            introMessage={{text: 'Send a chat message through an example server to OpenAI.'}}
            request={{url: '/api/openai/chat'}}
            requestBodyLimits={{maxMessages: 1}}
            errorMessages={{displayServiceErrorMessages: true}}
            requestInterceptor={(details: RequestDetails) => {
               if (details.body instanceof FormData) {
                  if (threadId.current) details.body.append('thread_id', JSON.stringify(threadId.current));
                } else if (threadId.current) {
                  details.body.thread_id = threadId.current;
                }
                return details;
            }}
            responseInterceptor={(response: Response & {thread_id: string}) => {
              threadId.current = response.thread_id;
              return response;
            }}
          />
        </div>
      </main>
    </>
  );
}
```
  
  
 ![+1](https://github.githubassets.com/assets/1f44d-41cb66fe1e22.png) 1 7h360df47h3r reacted with thumbs up emoji
-   ![+1](https://github.githubassets.com/assets/1f44d-41cb66fe1e22.png) 1 reaction
Owner
### 
**[OvidijusParsiunas](/OvidijusParsiunas)** commented [Nov 27, 2023](#issuecomment-1828385466)
Code for the [chat.ts](https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/nextjs/pages/api/openai/chat.ts) file. Make sure to set your `API_KEY` and `ASSISTANT_ID` variables:
```
import {DeepChatOpenAITextRequestBody} from '../../../types/deepChatTextRequestBody';
import {MessageContent} from 'deep-chat/dist/types/messages';
import errorHandler from '../../../utils/errorHandler';
import {NextRequest, NextResponse} from 'next/server';
import {
  OpenAIAssistantMessagesResult,
  OpenAIAssistantInitReqResult,
  OpenAIRunResult,
} from 'deep-chat/dist/types/openAIResult';
export const config = {
  runtime: 'edge',
};
const API_KEY = '';
const ASSISTANT_ID = '';
async function handler(req: NextRequest) {
  // Text messages are stored inside request body using the Deep Chat JSON format:
  // https://deepchat.dev/docs/connect
  const textRequestBody = (await req.json()) as {messages: MessageContent[]; thread_id?: string};
  console.log(textRequestBody);
  let thread_id: string = textRequestBody.thread_id;
  let run_id: string;
  if (thread_id) {
    const messageBody = createMessageBody(textRequestBody);
    // Create a new thread and automatically run it
    // https://platform.openai.com/docs/api-reference/messages/createMessage
    await fetch(`https://api.openai.com/v1/threads/${thread_id}/messages`, {
      headers: createHeaders(),
      method: 'POST',
      body: JSON.stringify(messageBody),
    });
    // https://platform.openai.com/docs/api-reference/runs/createRun
    const createAndRunResponse = await fetch(`https://api.openai.com/v1/threads/${thread_id}/runs`, {
      headers: createHeaders(),
      method: 'POST',
      body: JSON.stringify({assistant_id: ASSISTANT_ID}),
    });
    const createAndRunResult = (await createAndRunResponse.json()) as OpenAIAssistantInitReqResult;
    run_id = createAndRunResult.id;
  } else {
    const threadBody = createThreadBody(textRequestBody);
    // Create a new thread and automatically run it
    // https://platform.openai.com/docs/api-reference/runs/createThreadAndRun
    const createMessageAndRunResponse = await fetch('https://api.openai.com/v1/threads/runs', {
      headers: createHeaders(),
      method: 'POST',
      body: JSON.stringify(threadBody),
    });
    const createMessageAndRunResult = (await createMessageAndRunResponse.json()) as OpenAIAssistantInitReqResult;
    thread_id = createMessageAndRunResult.thread_id;
    run_id = createMessageAndRunResult.id;
  }
  // Get the result
  const resultText = await pollForResult(thread_id, run_id);
  // Sends response back to Deep Chat using the Response format:
  // https://deepchat.dev/docs/connect/#Response
  return NextResponse.json({text: resultText, thread_id: thread_id});
}
export function createThreadBody(body: DeepChatOpenAITextRequestBody) {
  // Text messages are stored inside request body using the Deep Chat JSON format:
  // https://deepchat.dev/docs/connect
  return {
    assistant_id: ASSISTANT_ID,
    thread: {
      messages: [
        {
          role: 'user',
          content: body.messages[body.messages.length - 1].text,
        },
      ],
    },
  };
}
export function createMessageBody(body: DeepChatOpenAITextRequestBody) {
  // Text messages are stored inside request body using the Deep Chat JSON format:
  // https://deepchat.dev/docs/connect
  return {
    role: 'user',
    content: body.messages[body.messages.length - 1].text,
  };
}
export function createHeaders() {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${API_KEY}`,
    'OpenAI-Beta': 'assistants=v1',
  };
}
async function pollForResult(thread_id: string, run_id: string) {
  // Get the run status
  // https://platform.openai.com/docs/api-reference/runs/listRuns
  const runStatusResponse = await fetch(`https://api.openai.com/v1/threads/${thread_id}/runs/${run_id}`, {
    headers: createHeaders(),
    method: 'GET',
  });
  const {status} = (await runStatusResponse.json()) as OpenAIRunResult;
  if (status === 'queued' || status === 'in_progress') {
    return await pollForResult(thread_id, run_id);
  } else if (status === 'completed') {
    // https://platform.openai.com/docs/api-reference/messages/listMessages
    const messagesResponse = await fetch(`https://api.openai.com/v1/threads/${thread_id}/messages`, {
      headers: createHeaders(),
      method: 'GET',
    });
    const messagesResult = (await messagesResponse.json()) as OpenAIAssistantMessagesResult;
    return messagesResult.data[0].content[0].text.value;
  }
  throw runStatusResponse.status;
}
export default errorHandler(handler);
```
  
  
 ![+1](https://github.githubassets.com/assets/1f44d-41cb66fe1e22.png) 1 7h360df47h3r reacted with thumbs up emoji
-   ![+1](https://github.githubassets.com/assets/1f44d-41cb66fe1e22.png) 1 reaction
Owner
### 
**[OvidijusParsiunas](/OvidijusParsiunas)** commented [Nov 27, 2023](#issuecomment-1828389958)
Important things to note are that we first create a `thread_id` and then re-use it for future conversations.
These examples should work right out of the box and you can tailor them to your use-case. If you have any questions specific to the OpenAI API, I recommend to instead check their documentation or use the [Developer Forum](https://community.openai.com/).
Let me know if you have any specific questions to the above examples. Thanks!
  
  
 ![heart](https://github.githubassets.com/assets/2764-982dc91ea48a.png) 1 7h360df47h3r reacted with heart emoji
-   ![heart](https://github.githubassets.com/assets/2764-982dc91ea48a.png) 1 reaction
[![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](/OvidijusParsiunas) [OvidijusParsiunas](/OvidijusParsiunas) closed this as [completed](/OvidijusParsiunas/deep-chat/issues?q=is%3Aissue+is%3Aclosed+archived%3Afalse+reason%3Acompleted) [Nov 27, 2023](#event-11074542291)
Author
### 
**[7h360df47h3r](/7h360df47h3r)** commented [Nov 27, 2023](#issuecomment-1828943445)
Perfect 💯 appreciate your time with this 🙏
May you assist finally with the same implementation using streaming, see [chat-stream.ts](https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/nextjs/pages/api/openai/chat-stream.ts).
  
  
Owner
### 
**[OvidijusParsiunas](/OvidijusParsiunas)** commented [Nov 28, 2023](#issuecomment-1829831552) •
edited
Edited 2 times
-    ![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&v=4) OvidijusParsiunas edited Nov 28, 2023 (most recent)
-    ![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&v=4) OvidijusParsiunas edited Nov 28, 2023
-    ![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&v=4) OvidijusParsiunas created Nov 28, 2023
The [chat-stream.ts](https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/nextjs/pages/api/openai/chat-stream.ts) file is designed to call a [Server Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) endpoint to stream the response back to the UI. [OpenAI Assistants](https://platform.openai.com/docs/api-reference/assistants) currently do not support streaming as noted in the [_Limitations_](https://platform.openai.com/docs/assistants/how-it-works/limitations) section of this [document](https://platform.openai.com/docs/assistants/how-it-works) - _"Support for streaming output (including Messages and Run Steps)."_.
However, instead you can simply keep the same code as you have in the [chat.ts](https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/nextjs/pages/api/openai/chat.ts) file and simply use the [`stream`](https://deepchat.dev/docs/connect#stream) property to _simulate_ the stream.  
All you will need to do is add the following property to Deep Chat in [index.ts](https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/nextjs/pages/index.tsx):  
`stream={{simulation: true}}`.
  
  
 ![+1](https://github.githubassets.com/assets/1f44d-41cb66fe1e22.png) 2 7h360df47h3r and techpeace reacted with thumbs up emoji
-   ![+1](https://github.githubassets.com/assets/1f44d-41cb66fe1e22.png) 2 reactions
Author
### 
**[7h360df47h3r](/7h360df47h3r)** commented [Nov 28, 2023](#issuecomment-1830040558)
I require guidance on integrating the new function calling methods using Assistant API into the above Next.js server example. Could you provide a simple example for this? Additionally, I am interested in offering financial support, but I noticed that GitHub doesn't accept PayPal for such transactions. Is there an alternative method to sponsor your work?
  
  
Owner
### 
**[OvidijusParsiunas](/OvidijusParsiunas)** commented [Nov 28, 2023](#issuecomment-1830424645) •
edited
Edited 6 times
-    ![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&v=4) OvidijusParsiunas edited Nov 28, 2023 (most recent)
-    ![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&v=4) OvidijusParsiunas edited Nov 28, 2023
-    ![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&v=4) OvidijusParsiunas edited Nov 28, 2023
-    ![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&v=4) OvidijusParsiunas edited Nov 28, 2023
-    ![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&v=4) OvidijusParsiunas edited Nov 28, 2023
-    ![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&v=4) OvidijusParsiunas edited Nov 28, 2023
-    ![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&v=4) OvidijusParsiunas created Nov 28, 2023
Don't worry about financial support.  
GitHub recently disabled direct sponsorships via PayPal in favour of Stripe, but if you really want to support you can use this email `oparsiunas@googlemail.com` for my PayPal. To note, I am motivated to work on this component by knowing that people are using it and every new GitHub Star keeps me going 🌟 . I am also just finishing up my career break and am looking for a job, so financially I will be ok. Thanks again for your kind thoughts!
When it comes to integrating functions/tools for Assistants API, majority of the setup really needs to be done when setting up your assistant. I recommend using the [Assistant Playground](https://platform.openai.com/playground) to first add your function:
[![Screenshot 2023-11-28 at 18 00 22](https://private-user-images.githubusercontent.com/18709577/286360101-1ad370d9-75ee-4618-ab8f-f5bb0215c3cd.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTA3MDYxMDUsIm5iZiI6MTcxMDcwNTgwNSwicGF0aCI6Ii8xODcwOTU3Ny8yODYzNjAxMDEtMWFkMzcwZDktNzVlZS00NjE4LWFiOGYtZjViYjAyMTVjM2NkLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDAzMTclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwMzE3VDIwMDMyNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTFhZTcxMjQwYTMzNGE4MDA3YmEwZDIzZGZiYjFlNGM2MDA0NDc4NDFmNWMxYjJjN2ZiZDRkNjI4YmRjZGEzNTkmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.K9QKbbcBuH_WCxtqSfnhSMOAeE033TZrVgZIhxUpqyw)](https://private-user-images.githubusercontent.com/18709577/286360101-1ad370d9-75ee-4618-ab8f-f5bb0215c3cd.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTA3MDYxMDUsIm5iZiI6MTcxMDcwNTgwNSwicGF0aCI6Ii8xODcwOTU3Ny8yODYzNjAxMDEtMWFkMzcwZDktNzVlZS00NjE4LWFiOGYtZjViYjAyMTVjM2NkLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDAzMTclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwMzE3VDIwMDMyNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTFhZTcxMjQwYTMzNGE4MDA3YmEwZDIzZGZiYjFlNGM2MDA0NDc4NDFmNWMxYjJjN2ZiZDRkNjI4YmRjZGEzNTkmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.K9QKbbcBuH_WCxtqSfnhSMOAeE033TZrVgZIhxUpqyw)
(This Asisstant is now removed as I used it for a demo)
After clicking the **Add** button, you will see a template for an example function setup code. This is where things get a little complicated as they require the understanding on what functions/tools are and how they are used. If you are new to them I recommend reading this [document](https://platform.openai.com/docs/assistants/tools/reading-the-functions-called-by-the-assistant) or watching this [video](https://www.youtube.com/watch?v=aqdWSYWC_LI&ab_channel=DaveEbbelaar) which really helped me (to note that vide is using the old API, but it helps understanding the concept of OpenAI functions).
When adding your function, you can just use the template, and for my case I have used a _get\_weather_ function which contains the following template:
```
{
  "name": "get_weather",
  "description": "Determine weather in my location",
  "parameters": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city and state e.g. San Francisco, CA"
      },
      "unit": {
        "type": "string",
        "enum": [
          "c",
          "f"
        ]
      }
    },
    "required": [
      "location"
    ]
  }
}
```
Given the function above, you can change the `pollForResult` function and add a new functions to the [chat.ts](https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/nextjs/pages/api/openai/chat.ts) example from above:
```
async function pollForResult(thread_id: string, run_id: string) {
  // Get the run status
  // https://platform.openai.com/docs/api-reference/runs/listRuns
  const runStatusResponse = await fetch(`https://api.openai.com/v1/threads/${thread_id}/runs/${run_id}`, {
    headers: createHeaders(),
    method: 'GET',
  });
  const {status, required_action} = (await runStatusResponse.json()) as OpenAIRunResult;
  if (status === 'queued' || status === 'in_progress') {
    return await pollForResult(thread_id, run_id);
  }
  if (status === 'completed') {
    // https://platform.openai.com/docs/api-reference/messages/listMessages
    const messagesResponse = await fetch(`https://api.openai.com/v1/threads/${thread_id}/messages`, {
      headers: createHeaders(),
      method: 'GET',
    });
    const messagesResult = (await messagesResponse.json()) as OpenAIAssistantMessagesResult;
    return messagesResult.data[0].content[0].text.value;
  }
  const toolCalls = required_action?.submit_tool_outputs?.tool_calls;
  if (status === 'requires_action' && toolCalls) {
    console.log('hello');
    return await handleTools(toolCalls, thread_id, run_id);
  }
  throw runStatusResponse.status;
}
async function handleTools(toolCalls: ToolCalls, thread_id: string, run_id: string) {
  const functions = toolCalls.map((call) => {
    return {name: call.function.name, arguments: call.function.arguments};
  });
  const handlerResponse = functions.map((functionDetails) => getCurrentWeather(functionDetails.arguments));
  const tool_outputs = handlerResponse.map((resp, index) => {
    return {tool_call_id: toolCalls[index].id, output: resp};
  });
  // https://platform.openai.com/docs/api-reference/runs/submitToolOutputs
  await fetch(`https://api.openai.com/v1/threads/${thread_id}/runs/${run_id}/submit_tool_outputs`, {
    headers: createHeaders(),
    method: 'POST',
    body: JSON.stringify({tool_outputs}),
  });
  await new Promise((resolve) => setTimeout(resolve, 1000)); // wait for OpenAI to read the output
  return await pollForResult(thread_id, run_id);
}
function getCurrentWeather(location: string) {
  location = location.toLowerCase();
  if (location.includes('tokyo')) {
    return 'Good';
  }
  if (location.includes('san francisco')) {
    return 'Mild';
  }
  return 'Very Hot';
}
```
In this example the `getCurrentWeather` function is what handles the actual output.
Once you have all the code that is setup, this should work as follows:
[![image](https://private-user-images.githubusercontent.com/18709577/286359048-0e4a4580-4a15-41dc-adaa-3ba2ffe29c29.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTA3MDYxMDUsIm5iZiI6MTcxMDcwNTgwNSwicGF0aCI6Ii8xODcwOTU3Ny8yODYzNTkwNDgtMGU0YTQ1ODAtNGExNS00MWRjLWFkYWEtM2JhMmZmZTI5YzI5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDAzMTclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwMzE3VDIwMDMyNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWE1MDdmMWRiZGQ1ZGI0ZGU4OTUzMDEwODcyMjFiNjg3ZThlYmY0ZDc3Mzg1YjRmMTQ0YWU3YmJjMWY3MWNkM2EmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.HpiAJ2CVRN7MEQ_pN043WKsT1OdMWdTW6K67px5HbBs)](https://private-user-images.githubusercontent.com/18709577/286359048-0e4a4580-4a15-41dc-adaa-3ba2ffe29c29.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTA3MDYxMDUsIm5iZiI6MTcxMDcwNTgwNSwicGF0aCI6Ii8xODcwOTU3Ny8yODYzNTkwNDgtMGU0YTQ1ODAtNGExNS00MWRjLWFkYWEtM2JhMmZmZTI5YzI5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDAzMTclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwMzE3VDIwMDMyNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWE1MDdmMWRiZGQ1ZGI0ZGU4OTUzMDEwODcyMjFiNjg3ZThlYmY0ZDc3Mzg1YjRmMTQ0YWU3YmJjMWY3MWNkM2EmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.HpiAJ2CVRN7MEQ_pN043WKsT1OdMWdTW6K67px5HbBs)
**To note, the Assistants tools API does not always work and sometimes it is unable to read the function response, but the code in this example is correct**
Hopefully this helps you!
  
  
 ![heart](https://github.githubassets.com/assets/2764-982dc91ea48a.png) 2 7h360df47h3r and techpeace reacted with heart emoji
-   ![heart](https://github.githubassets.com/assets/2764-982dc91ea48a.png) 2 reactions
Author
### 
**[7h360df47h3r](/7h360df47h3r)** commented [Nov 29, 2023](#issuecomment-1831169459)
This has helped me greatly thank you.
  
  
[![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](/OvidijusParsiunas) [OvidijusParsiunas](/OvidijusParsiunas) changed the title Support Passing Assistant Details in the Custom Requests OpenAI Assistant in a proxy server [Dec 29, 2023](#event-11358973620)
[![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](/OvidijusParsiunas) [OvidijusParsiunas](/OvidijusParsiunas) mentioned this issue [Dec 29, 2023](#ref-issue-2060405685)
[OpenAI Assistant through a proxy #82](/OvidijusParsiunas/deep-chat/issues/82)
Closed
### 
**[AhmeedBen](/AhmeedBen)** commented [Jan 13, 2024](#issuecomment-1890598901)
thanks, this works fine with text messages, what about files upload ?
  
  
Owner
### 
**[OvidijusParsiunas](/OvidijusParsiunas)** commented [Jan 13, 2024](#issuecomment-1890748168) •
edited
Edited 3 times
-    ![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&v=4) OvidijusParsiunas edited Jan 15, 2024 (most recent)
-    ![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&v=4) OvidijusParsiunas edited Jan 14, 2024
-    ![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&v=4) OvidijusParsiunas edited Jan 14, 2024
-    ![@OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&v=4) OvidijusParsiunas created Jan 13, 2024
Hi [@AhmeedBen](https://github.com/AhmeedBen).
To upload files, the first thing you will need to do is enable the [`mixedFiles`](https://deepchat.dev/docs/files#mixedFiles) (or any other that suits your use-case better) property on the Deep Chat component.
When you send files from Deep Chat, you must remember that the request format is encapsulated inside [FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData) as referenced in the [Request message](https://deepchat.dev/docs/connect) section.
Here is the new [chat.ts](https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/nextjs/pages/api/openai/chat.ts) code:
```
import {DeepChatOpenAITextRequestBody} from '../../../types/deepChatTextRequestBody';
import errorHandler from '../../../utils/errorHandler';
import {NextRequest, NextResponse} from 'next/server';
import {
  OpenAIAssistantMessagesResult,
  OpenAIAssistantInitReqResult,
  OpenAIRunResult,
} from 'deep-chat/dist/types/openAIResult';
export const config = {
  runtime: 'edge',
};
const API_KEY = '';
const ASSISTANT_ID = '';
async function handler(req: NextRequest) {
  const formData = await req.formData();
  // aggregate data
  const files: File[] = [];
  const textRequestBody: DeepChatOpenAITextRequestBody = {messages: []};
  let thread_id: string | undefined;
  formData.forEach((data) => {
    if (typeof data === 'object') {
      files.push(data);
    } else {
      const parsedData = JSON.parse(data);
      if (typeof parsedData === 'string') {
        thread_id = parsedData;
      } else {
        textRequestBody.messages.push(parsedData);
      }
    }
  });
  // store files
  const file_ids = files ? await storeFiles(files) : undefined;
  let run_id: string;
  if (thread_id) {
    const messageBody = createMessageBody(textRequestBody, file_ids);
    // Create a new message
    // https://platform.openai.com/docs/api-reference/messages/createMessage
    await fetch(`https://api.openai.com/v1/threads/${thread_id}/messages`, {
      headers: createHeaders(),
      method: 'POST',
      body: JSON.stringify(messageBody),
    });
    // https://platform.openai.com/docs/api-reference/runs/createRun
    const createAndRunResponse = await fetch(`https://api.openai.com/v1/threads/${thread_id}/runs`, {
      headers: createHeaders(),
      method: 'POST',
      body: JSON.stringify({assistant_id: ASSISTANT_ID}),
    });
    const createAndRunResult = (await createAndRunResponse.json()) as OpenAIAssistantInitReqResult;
    run_id = createAndRunResult.id;
  } else {
    const threadBody = createThreadBody(textRequestBody, file_ids);
    // Create a new thread and automatically run it
    // https://platform.openai.com/docs/api-reference/runs/createThreadAndRun
    const createMessageAndRunResponse = await fetch('https://api.openai.com/v1/threads/runs', {
      headers: createHeaders(),
      method: 'POST',
      body: JSON.stringify(threadBody),
    });
    const createMessageAndRunResult = (await createMessageAndRunResponse.json()) as OpenAIAssistantInitReqResult;
    thread_id = createMessageAndRunResult.thread_id;
    run_id = createMessageAndRunResult.id;
  }
  // Get the result
  const resultText = await pollForResult(thread_id, run_id);
  // Sends response back to Deep Chat using the Response format:
  // https://deepchat.dev/docs/connect/#Response
  return NextResponse.json({text: resultText, thread_id: thread_id});
}
async function storeFiles(files: File[]) {
  const headers = createHeaders();
  delete headers['Content-Type']; // don't need when sending files
  const requests = files.map(async (file) => {
    const formData = new FormData();
    formData.append('purpose', 'assistants');
    formData.append('file', file);
    return new Promise<{id: string}>(async (resolve) => {
      const response = await fetch('https://api.openai.com/v1/files', {headers, method: 'POST', body: formData});
      const content = await response.json();
      resolve(content);
    });
  });
  try {
    return (await Promise.all(requests)).map((result) => result.id);
  } catch (err) {
    console.log('error');
    console.log(err);
  }
}
export function createThreadBody(body: DeepChatOpenAITextRequestBody, file_ids: string[]) {
  // Text messages are stored inside request body using the Deep Chat JSON format:
  // https://deepchat.dev/docs/connect
  return {
    assistant_id: ASSISTANT_ID,
    thread: {
      messages: [
        {
          role: 'user',
          content: body.messages[body.messages.length - 1].text,
          file_ids,
        },
      ],
    },
  };
}
export function createMessageBody(body: DeepChatOpenAITextRequestBody, file_ids: string[]) {
  // Text messages are stored inside request body using the Deep Chat JSON format:
  // https://deepchat.dev/docs/connect
  return {
    role: 'user',
    content: body.messages[body.messages.length - 1].text,
    file_ids,
  };
}
export function createHeaders() {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${API_KEY}`,
    'OpenAI-Beta': 'assistants=v1',
  };
}
async function pollForResult(thread_id: string, run_id: string) {
  // Get the run status
  // https://platform.openai.com/docs/api-reference/runs/listRuns
  const runStatusResponse = await fetch(`https://api.openai.com/v1/threads/${thread_id}/runs/${run_id}`, {
    headers: createHeaders(),
    method: 'GET',
  });
  const {status} = (await runStatusResponse.json()) as OpenAIRunResult;
  if (status === 'queued' || status === 'in_progress') {
    return await pollForResult(thread_id, run_id);
  } else if (status === 'completed') {
    // https://platform.openai.com/docs/api-reference/messages/listMessages
    const messagesResponse = await fetch(`https://api.openai.com/v1/threads/${thread_id}/messages`, {
      headers: createHeaders(),
      method: 'GET',
    });
    const messagesResult = (await messagesResponse.json()) as OpenAIAssistantMessagesResult;
    return messagesResult.data[0].content[0].text.value;
  }
  throw runStatusResponse.status;
}
export default errorHandler(handler);
```
  
  
### 
**[AhmeedBen](/AhmeedBen)** commented [Jan 13, 2024](#issuecomment-1890761925)
I tried the code but still get the error:  
API Error: \[SyntaxError: Unexpected token 'o', "\[object File\]" is not valid JSON\]  
text messages works fine
  
  
Owner
### 
**[OvidijusParsiunas](/OvidijusParsiunas)** commented [Jan 13, 2024](#issuecomment-1890779874)
It could be that your assistant is not configured to work with files, does uploading files work for you in [OpenAI Playground](https://platform.openai.com/playground)?
  
  
### 
**[AhmeedBen](/AhmeedBen)** commented [Jan 14, 2024](#issuecomment-1890968738)
yes the assistant works with files in the playground.
  
  
Owner
### 
**[OvidijusParsiunas](/OvidijusParsiunas)** commented [Jan 14, 2024](#issuecomment-1890972462)
I just tested the code I commented above and it works fine for me.
It is hard say what is causing your issue, but if you have copied the code exactly as described then it is definitely something else. I would recommend to make sure that the `API_KEY` and the `ASSISTANT_ID` have been set correctly.
Could you perhaps share the prompt you are using, what kind of files you are uploading and what kind of response you expect to get?
Other than this, the amount of support I can provide is limited, however if you try to debug your app and find the line that is causing the error that would be helpful.
Thanks.
  
  
### 
**[AhmeedBen](/AhmeedBen)** commented [Jan 14, 2024](#issuecomment-1890991895)
the execution stops here:
formData.forEach((data) => {  
if (data instanceof File) {  
files.push(data);  
} else {  
textRequestBody.messages.push(JSON.parse(data) as MessageContent);  
}  
});
the first condition is not fulfiled, despite of uploading file
  
  
Owner
### 
**[OvidijusParsiunas](/OvidijusParsiunas)** commented [Jan 14, 2024](#issuecomment-1890994295)
That is very strange, for some reason the `data` is not recognised as a file.  
Is your `index.tsx` file different than the one in [this comment](https://github.com/OvidijusParsiunas/deep-chat/issues/53#issuecomment-1828383196). Ofcourse with the addition of [mixedFiles](https://deepchat.dev/docs/files#mixedFiles).
  
  
### 
**[AhmeedBen](/AhmeedBen)** commented [Jan 14, 2024](#issuecomment-1890995048)
I changed the condition to typeof data === 'object' , and it works fine,  
I don't know this will affect the other types of uploads.
  
  
Owner
### 
**[OvidijusParsiunas](/OvidijusParsiunas)** commented [Jan 14, 2024](#issuecomment-1891062746)
Happy to hear it works for you, I have also updated my example to reflect this. Thankyou!
  
  
### 
**[AhmeedBen](/AhmeedBen)** commented [Jan 15, 2024](#issuecomment-1891536257)
Thank you very much,  
Another thing, a new thread is created everytime we add a new file.  
I tried to use  
const textRequestBody = (await req.json()) as {messages: \[\]; thread\_id?: string};  
but it doesn't work.
  
  
Owner
### 
**[OvidijusParsiunas](/OvidijusParsiunas)** commented [Jan 15, 2024](#issuecomment-1892859628)
I have updated the `chat.ts` and `index.tsx` examples to help handle the same thread\_id (session) form FormData.
  
  
### 
**[AhmeedBen](/AhmeedBen)** commented [Jan 16, 2024](#issuecomment-1893272301)
Thank you very much, everything works fine now.
