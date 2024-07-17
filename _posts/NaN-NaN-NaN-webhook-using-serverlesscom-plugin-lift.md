---
tags:
  - serverless
info: aberto.
date: NaN-NaN-NaN
type: post
layout: post
published: true
slug: webhook-using-serverlesscom-plugin-lift
title: 'Webhook using Serverless.com plugin: Lift'
---

***
serverless.yml

```yml
service: github-webhook-service

provider:
  name: aws
  runtime: nodejs20.x
  region: us-east-1
  environment:
    GITHUB_TOKEN: ${env:GITHUB_TOKEN}
    
plugins:
  - serverless-lift

constructs:
  webhook:
    type: webhook
    path: /webhook
    method: POST
    eventType: $request.body.type
    insecure: true

functions:
  handleWebhook:
    handler: handler.handleWebhook
    events:
      - eventBridge:
          eventBus: ${construct:webhook.busName}
          pattern:
            source:
              - webhook
            detail-type:
              - new_comment
    
package:
  patterns:
    - '!node_modules/aws-sdk/**'
    - '!node_modules/@aws-sdk/**'
```
***

---
handler.mjs

~~~mjs
import { Octokit } from "@octokit/rest";
import { Base64 } from "js-base64";

// Utility function to slugify a string
const slugify = (str) => {
  return str
    .toString()
    .toLowerCase()
    .replace(/\s+/g, '-') // Replace spaces with -
    .replace(/[^\w\-]+/g, '') // Remove all non-word chars
    .replace(/\-\-+/g, '-') // Replace multiple - with single -
    .replace(/^-+/, '') // Trim - from start of text
    .replace(/-+$/, ''); // Trim - from end of text
};

// Utility function to format date to YYYY-MM-DD
const formatDate = (dateString) => {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

// Function to create markdown content with the provided template
const createPostContent = (data) => {
  const { by_nickname, by_email, content, time } = data;
  const slugName = slugify(by_nickname);
  const date = formatDate(time);

  return `---
tags:
  - ${by_email}
info: aberto.
date: ${date}
type: post
layout: post
published: true
slug: ${slugName}
title: '${by_nickname}'
---

${content}`;
};

// Handler function for the webhook
export const handleWebhook = async (event) => {
  const detail = event.detail;
  const { by_nickname, by_email, content, time } = detail.data;

  // Validate required fields
  if (!by_email) {
    return {
      statusCode: 400,
      body: JSON.stringify({ message: "Email is required" }),
    };
  }

  const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

  const owner = "${REPO_OWNER}";
  const repo = "${REPO_NAME}";
  const path = `_posts/${formatDate(time)}-${slugify(by_nickname)}.md`;
  const message = `New post by ${by_nickname}`;
  const postContent = createPostContent({ by_nickname, by_email, content, time });
  const contentEncoded = Base64.encode(postContent);

  try {
    await octokit.repos.createOrUpdateFileContents({
      owner,
      repo,
      path,
      message,
      content: contentEncoded,
    });

    return {
      statusCode: 200,
      body: JSON.stringify({ message: "File created/updated successfully" }),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ message: error.message }),
    };
  }
};

~~~
---