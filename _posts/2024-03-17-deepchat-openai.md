---
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

Title: OpenAI Assistant in a proxy server · Issue #53 · OvidijusParsiunas/deep-chat

URL Source: https://github.com/OvidijusParsiunas/deep-chat/issues/53

Markdown Content:
OpenAI Assistant in a proxy server #53
--------------------------------------

Assignees

[![Image 1: @OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&v=4)](https://github.com/OvidijusParsiunas)

Labels

[advice](https://github.com/OvidijusParsiunas/deep-chat/labels/advice)

Information how to use/implement the component

Comments
--------

[![Image 2: @7h360df47h3r](https://avatars.githubusercontent.com/u/93761786?s=80&u=69a6f6a3ffd946631a513185b49f37ecf0d8b38f&v=4)](https://github.com/7h360df47h3r)

### Feature Request: Support Passing Assistant Details in Custom Requests

**Current Behavior:**  
I am utilising your deep-chat-nextjs server as a proxy for OpenAI and the `request` prop in the `DeepChat` component does not support assistant parameters like the Direct Connection for OpenAI.

**Desired Behavior:**  
I would like to request support for passing assistant details in the `request` prop.

**Additional Information**  
If an update is not feasible, it would be greatly appreciated if you could provide guidance on how to achieve the requested functionality manually using custom headers and what it would look like on the nextjs example server.

[![Image 3: @OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=80&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](https://github.com/OvidijusParsiunas)

Hi. When connecting Deep Chat to your own backend (like a NextJs function), the specific code for calling another service such as [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview) should be written in the backend and not in Deep Chat.

We try to keep the backend examples as simple as possible so that developers can tailor them to their use-cases, hence we would prefer not to expand our examples for this reason.

In regards to your specific problem, connecting to [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview) is a quite complex task as it requires the use of the [Assistants](https://platform.openai.com/docs/api-reference/assistants), [Threads](https://platform.openai.com/docs/api-reference/threads), [Messages](https://platform.openai.com/docs/api-reference/messages) and [Runs](https://platform.openai.com/docs/api-reference/runs) APIs.

If you want to do this manually in your own backend, you can use the code that I will paste below.

[![Image 4: @OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=80&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](https://github.com/OvidijusParsiunas)

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

[![Image 5: @OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=80&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](https://github.com/OvidijusParsiunas)

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

[![Image 6: @OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=80&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](https://github.com/OvidijusParsiunas)

Important things to note are that we first create a `thread_id` and then re-use it for future conversations.

These examples should work right out of the box and you can tailor them to your use-case. If you have any questions specific to the OpenAI API, I recommend to instead check their documentation or use the [Developer Forum](https://community.openai.com/).

Let me know if you have any specific questions to the above examples. Thanks!

[![Image 7: @7h360df47h3r](https://avatars.githubusercontent.com/u/93761786?s=80&u=69a6f6a3ffd946631a513185b49f37ecf0d8b38f&v=4)](https://github.com/7h360df47h3r)

Perfect 💯 appreciate your time with this 🙏

May you assist finally with the same implementation using streaming, see [chat-stream.ts](https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/nextjs/pages/api/openai/chat-stream.ts).

[![Image 8: @OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=80&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](https://github.com/OvidijusParsiunas)

The [chat-stream.ts](https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/nextjs/pages/api/openai/chat-stream.ts) file is designed to call a [Server Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) endpoint to stream the response back to the UI. [OpenAI Assistants](https://platform.openai.com/docs/api-reference/assistants) currently do not support streaming as noted in the [_Limitations_](https://platform.openai.com/docs/assistants/how-it-works/limitations) section of this [document](https://platform.openai.com/docs/assistants/how-it-works) - _"Support for streaming output (including Messages and Run Steps)."_.

However, instead you can simply keep the same code as you have in the [chat.ts](https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/nextjs/pages/api/openai/chat.ts) file and simply use the [`stream`](https://deepchat.dev/docs/connect#stream) property to _simulate_ the stream.  
All you will need to do is add the following property to Deep Chat in [index.ts](https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/nextjs/pages/index.tsx):  
`stream={{simulation: true}}`.

[![Image 9: @7h360df47h3r](https://avatars.githubusercontent.com/u/93761786?s=80&u=69a6f6a3ffd946631a513185b49f37ecf0d8b38f&v=4)](https://github.com/7h360df47h3r)

I require guidance on integrating the new function calling methods using Assistant API into the above Next.js server example. Could you provide a simple example for this? Additionally, I am interested in offering financial support, but I noticed that GitHub doesn't accept PayPal for such transactions. Is there an alternative method to sponsor your work?

[![Image 10: @OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=80&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](https://github.com/OvidijusParsiunas)

Don't worry about financial support.  
GitHub recently disabled direct sponsorships via PayPal in favour of Stripe, but if you really want to support you can use this email `oparsiunas@googlemail.com` for my PayPal. To note, I am motivated to work on this component by knowing that people are using it and every new GitHub Star keeps me going 🌟 . I am also just finishing up my career break and am looking for a job, so financially I will be ok. Thanks again for your kind thoughts!

When it comes to integrating functions/tools for Assistants API, majority of the setup really needs to be done when setting up your assistant. I recommend using the [Assistant Playground](https://platform.openai.com/playground) to first add your function:

[![Image 11: Screenshot 2023-11-28 at 18 00 22](https://private-user-images.githubusercontent.com/18709577/286360101-1ad370d9-75ee-4618-ab8f-f5bb0215c3cd.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTkyNjYwMzcsIm5iZiI6MTcxOTI2NTczNywicGF0aCI6Ii8xODcwOTU3Ny8yODYzNjAxMDEtMWFkMzcwZDktNzVlZS00NjE4LWFiOGYtZjViYjAyMTVjM2NkLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA2MjQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNjI0VDIxNDg1N1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWRmNGRkMjM5NDlmOTBhN2E4ODI3Yjk1YmU2NjQ3OThjMGExYzc0ZmY5NTc1MGNkMTUzZTEwN2IyY2Y4NDg1YzImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.Rfaa9tmyZ8rlnyDsLvUa3gJ-Ba5v9PQaeBzD3Ok3qqA)](https://private-user-images.githubusercontent.com/18709577/286360101-1ad370d9-75ee-4618-ab8f-f5bb0215c3cd.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTkyNjYwMzcsIm5iZiI6MTcxOTI2NTczNywicGF0aCI6Ii8xODcwOTU3Ny8yODYzNjAxMDEtMWFkMzcwZDktNzVlZS00NjE4LWFiOGYtZjViYjAyMTVjM2NkLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA2MjQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNjI0VDIxNDg1N1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWRmNGRkMjM5NDlmOTBhN2E4ODI3Yjk1YmU2NjQ3OThjMGExYzc0ZmY5NTc1MGNkMTUzZTEwN2IyY2Y4NDg1YzImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.Rfaa9tmyZ8rlnyDsLvUa3gJ-Ba5v9PQaeBzD3Ok3qqA)(This Asisstant is now removed as I used it for a demo)

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

[![Image 12: image](https://private-user-images.githubusercontent.com/18709577/286359048-0e4a4580-4a15-41dc-adaa-3ba2ffe29c29.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTkyNjYwMzcsIm5iZiI6MTcxOTI2NTczNywicGF0aCI6Ii8xODcwOTU3Ny8yODYzNTkwNDgtMGU0YTQ1ODAtNGExNS00MWRjLWFkYWEtM2JhMmZmZTI5YzI5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA2MjQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNjI0VDIxNDg1N1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTk2YjYzYTZkMGI5MTdjYTI4YjQ4YzMxYzY0YWJiN2RiZDM1YmQxYjIyYTQxYzEzMTIyMzU2ZWFmMjgwNDU2NzAmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.deMo-hzPoVvQxjw4kouwvhJbHTkJc6LoLe4CdPHuFL4)](https://private-user-images.githubusercontent.com/18709577/286359048-0e4a4580-4a15-41dc-adaa-3ba2ffe29c29.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTkyNjYwMzcsIm5iZiI6MTcxOTI2NTczNywicGF0aCI6Ii8xODcwOTU3Ny8yODYzNTkwNDgtMGU0YTQ1ODAtNGExNS00MWRjLWFkYWEtM2JhMmZmZTI5YzI5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA2MjQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNjI0VDIxNDg1N1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTk2YjYzYTZkMGI5MTdjYTI4YjQ4YzMxYzY0YWJiN2RiZDM1YmQxYjIyYTQxYzEzMTIyMzU2ZWFmMjgwNDU2NzAmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.deMo-hzPoVvQxjw4kouwvhJbHTkJc6LoLe4CdPHuFL4)**To note, the Assistants tools API does not always work and sometimes it is unable to read the function response, but the code in this example is correct**

Hopefully this helps you!

[![Image 13: @7h360df47h3r](https://avatars.githubusercontent.com/u/93761786?s=80&u=69a6f6a3ffd946631a513185b49f37ecf0d8b38f&v=4)](https://github.com/7h360df47h3r)

This has helped me greatly thank you.

[![Image 14: @OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=40&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](https://github.com/OvidijusParsiunas) [OvidijusParsiunas](https://github.com/OvidijusParsiunas) changed the title Support Passing Assistant Details in the Custom Requests OpenAI Assistant in a proxy server

[Dec 29, 2023](https://github.com/OvidijusParsiunas/deep-chat/issues/53#event-11358973620)

[![Image 15: @AhmeedBen](https://avatars.githubusercontent.com/u/130488191?s=80&v=4)](https://github.com/AhmeedBen)

thanks, this works fine with text messages, what about files upload ?

[![Image 16: @OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=80&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](https://github.com/OvidijusParsiunas)

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

[![Image 17: @AhmeedBen](https://avatars.githubusercontent.com/u/130488191?s=80&v=4)](https://github.com/AhmeedBen)

I tried the code but still get the error:  
API Error: \[SyntaxError: Unexpected token 'o', "\[object File\]" is not valid JSON\]  
text messages works fine

[![Image 18: @OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=80&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](https://github.com/OvidijusParsiunas)

It could be that your assistant is not configured to work with files, does uploading files work for you in [OpenAI Playground](https://platform.openai.com/playground)?

[![Image 19: @AhmeedBen](https://avatars.githubusercontent.com/u/130488191?s=80&v=4)](https://github.com/AhmeedBen)

yes the assistant works with files in the playground.

[![Image 20: @OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=80&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](https://github.com/OvidijusParsiunas)

I just tested the code I commented above and it works fine for me.

It is hard say what is causing your issue, but if you have copied the code exactly as described then it is definitely something else. I would recommend to make sure that the `API_KEY` and the `ASSISTANT_ID` have been set correctly.

Could you perhaps share the prompt you are using, what kind of files you are uploading and what kind of response you expect to get?

Other than this, the amount of support I can provide is limited, however if you try to debug your app and find the line that is causing the error that would be helpful.

Thanks.

[![Image 21: @AhmeedBen](https://avatars.githubusercontent.com/u/130488191?s=80&v=4)](https://github.com/AhmeedBen)

the execution stops here:

formData.forEach((data) => {  
if (data instanceof File) {  
files.push(data);  
} else {  
textRequestBody.messages.push(JSON.parse(data) as MessageContent);  
}  
});

the first condition is not fulfiled, despite of uploading file

[![Image 22: @OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=80&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](https://github.com/OvidijusParsiunas)

That is very strange, for some reason the `data` is not recognised as a file.  
Is your `index.tsx` file different than the one in [this comment](https://github.com/OvidijusParsiunas/deep-chat/issues/53#issuecomment-1828383196). Ofcourse with the addition of [mixedFiles](https://deepchat.dev/docs/files#mixedFiles).

[![Image 23: @AhmeedBen](https://avatars.githubusercontent.com/u/130488191?s=80&v=4)](https://github.com/AhmeedBen)

I changed the condition to typeof data === 'object' , and it works fine,  
I don't know this will affect the other types of uploads.

[![Image 24: @OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=80&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](https://github.com/OvidijusParsiunas)

Happy to hear it works for you, I have also updated my example to reflect this. Thankyou!

[![Image 25: @AhmeedBen](https://avatars.githubusercontent.com/u/130488191?s=80&v=4)](https://github.com/AhmeedBen)

Thank you very much,  
Another thing, a new thread is created everytime we add a new file.  
I tried to use  
const textRequestBody = (await req.json()) as {messages: \[\]; thread\_id?: string};  
but it doesn't work.

[![Image 26: @OvidijusParsiunas](https://avatars.githubusercontent.com/u/18709577?s=80&u=245fd9851eb14ce9a588180ba9234a50544cb07c&v=4)](https://github.com/OvidijusParsiunas)

I have updated the `chat.ts` and `index.tsx` examples to help handle the same thread\_id (session) form FormData.

[![Image 27: @AhmeedBen](https://avatars.githubusercontent.com/u/130488191?s=80&v=4)](https://github.com/AhmeedBen)

Thank you very much, everything works fine now.

Labels

[advice](https://github.com/OvidijusParsiunas/deep-chat/labels/advice)

Information how to use/implement the component
