---
tags:
  - tasks
info: aberto.
date: 2024-09-12
type: post
layout: post
published: true
slug: mlo-setup-using-ratzs-computed-score-algorithm
title: 'MLO setup using Ratz's Computed-Score Algorithm'
---

#### **1. Structure Your Task Hierarchy**
Start by building a clear task hierarchy where each **parent task** is broken down into **subtasks**. This structure will help you localize the prioritization process, making it easier to manage tasks in relation to their parent task.

- **Create a logical outline** of your tasks. Each **project** or **major goal** should be a **parent task** at the top level, with **subtasks** underneath it that contribute to completing the parent task.
  
  **Example**:
  - **Parent Task**: Write a Research Paper
    - **Subtask 1**: Conduct Research
    - **Subtask 2**: Write Introduction
    - **Subtask 3**: Write Body
    - **Subtask 4**: Proofread and Edit

---

#### **2. Only Set Importance for Tasks with Siblings**
To keep the system efficient and avoid unnecessary complexity, **Ratz** advises **only setting importance for tasks that have siblings**. This means you should focus on comparing tasks that are at the **same level** under the same **parent task**.

- **If a task has no siblings**, you **don’t need to set its importance** manually. It will **automatically inherit** the importance of its parent task.
  
- **If a task has siblings**, then you need to set the importance slider for those tasks to determine which is more important **relative to the parent task**.

#### **Example**:
- Under the parent task **"Write a Research Paper"**, you have four subtasks:
  - **Subtask 1**: Conduct Research
  - **Subtask 2**: Write Introduction
  - **Subtask 3**: Write Body
  - **Subtask 4**: Proofread and Edit

Since these subtasks are **siblings**, you need to decide which one is more important **relative to the parent task**. For example, **Conduct Research** might be more important than **Write Introduction**, so you would set the importance slider higher for **Conduct Research**.

- **If a task does not have siblings**, like if **Subtask 1** had no other subtasks, there’s no need to set its importance. It will simply inherit the importance of **"Write a Research Paper"**.

---

#### **3. Set the Importance Slider for Parent Tasks**
Once you’ve structured your task hierarchy and identified which tasks have siblings, the next step is to set the **importance** for your **parent tasks**. The **parent tasks** should be ranked based on how important they are **relative to each other**.

- **Ask yourself**: How important is this parent task compared to the other parent tasks in this outline?
  
  - **Move the importance slider** accordingly. For highly important parent tasks, slide it towards the right. For less important parent tasks, slide it towards the left.
  
  **Example**:
  - If **"Write a Research Paper"** is more important than another parent task like **"Clean the House"**, you might set the importance slider for **"Write a Research Paper"** higher.

---

#### **4. Set the Importance Slider for Sibling Subtasks**
Now that you’ve set the importance for the parent tasks, focus on the **subtasks** that have **siblings**. Remember, **only set the importance for sibling tasks**. The importance should reflect **how crucial each sibling task is to completing the parent task**.

- **Ask yourself**: How important is each sibling task for completing the parent task?
  
  - **Move the importance slider** for each sibling task based on its importance to completing the parent task. Subtasks that are critical for completing the parent task should have a higher importance, while less critical subtasks should have lower importance.

#### **Example**:
- Under the parent task **"Write a Research Paper"**, you have four subtasks:
  - **Subtask 1**: Conduct Research
  - **Subtask 2**: Write Introduction
  - **Subtask 3**: Write Body
  - **Subtask 4**: Proofread and Edit

Since these are **siblings**, you need to decide their relative importance. **Conduct Research** might be the most important because it forms the foundation for the rest of the tasks. So, you would set its importance higher than **Write Introduction** or **Proofread and Edit**.

---

#### **5. Use Start and Due Dates to Manipulate Urgency**
In **Ratz’s** system, **urgency** is naturally calculated based on the **start date** and **due date** of the task. There’s no need for artificial urgency boosts like the `weekly goal` or `overdue boost`. As the due date approaches, the urgency of the task increases automatically.

Here’s how to effectively use **start dates** and **due dates** to control urgency:

- **Set a realistic start date** for tasks that need attention over time. The urgency of the task will start to increase once the start date is reached, and will continue to increase as the due date approaches.
  
- **Set a due date** that reflects when the task needs to be completed. As the due date gets closer, the urgency will naturally increase, and if the task becomes overdue, urgency will continue to rise.
  
  **Example**:
  - For the task **"Conduct Research"**, set a **start date** for when you plan to begin the research and a **due date** for when the research needs to be completed. As the due date approaches, **MLO** will automatically boost the urgency of this task, helping you prioritize it appropriately.

#### **Important Tip**:
- Be **realistic** with your start and due dates. Don’t set arbitrary dates just to manipulate urgency. Set dates that genuinely reflect when you plan to start and when the task must be completed. This ensures that urgency increases at the right time.

---

#### **6. Adjust Preferences for Date-Based Weighting**
To fully leverage **start and due dates** for urgency calculations, you’ll want to adjust the **date-based weighting factors** in the MLO preferences. These settings control how much influence start and due dates have on urgency.

- **Go to MLO Preferences** and adjust the **Start Date Weighting Factor** and **Due Date Weighting Factor**.
  
  - **Start Date Weighting**: Controls how much the start date influences urgency. Increase this if you want tasks to start becoming urgent once the start date is reached.
  
  - **Due Date Weighting**: Controls how much the due date influences urgency. Increase this if you want tasks to become highly urgent as the due date approaches.
  
  **Example**:
  - If you want the urgency of tasks to significantly increase as the due date approaches, set a **high weighting** for the due date. If you want tasks to become urgent earlier, increase the **start date weighting**.

#### **Best Practice**:
- Start with **moderate values** for the weighting factors and observe how they influence your task list. You can adjust them over time to better suit your workflow.

---

#### **7. Combine Importance and Urgency to Calculate Priority**
Once you’ve set the **importance** and **urgency** for each task, **MLO** will calculate the **Computed-Score Priority** based on the product of these two values. This ensures that tasks with both high importance and high urgency rise to the top of your **To-Do List**.

- **Formula**: 
  \[
  \text{Score} = (\text{Importance Score} \times \text{Urgency Score}) + \text{Date Score Contribution}
  \]
  
  - **Importance Score**: Based on the **importance slider** you set.
  - **Urgency Score**: Based on the **start date** and **due date**.
  - **Date Score Contribution**: The influence of the start and due dates based on the weighting factors you set.

---

#### **8. Review the To-Do List and Adjust if Necessary**
After setting the importance and urgency values, **MLO** will generate a **To-Do List** ordered by **Computed-Score Priority**. The tasks at the top of the list will be those with the highest combined importance and urgency.

- **Review the list** to ensure that the most critical tasks are appearing at the top.
  
- If the order doesn’t seem right, go back to the **Outline view** and adjust the **importance sliders** or **start/due dates**. Remember, adjustments should be made in the **Outline view** where you can see the entire task hierarchy — not in the **To-Do List** itself.

---

#### **9. Avoid Over-Tweaking**
One of **Ratz’s** key recommendations is to **avoid over-tweaking**. Don’t constantly adjust the importance and urgency values based on what you see in the **To-Do List**. If you find that tasks are not appearing in the right order, the issue is likely in the **Outline** (the structure of your task hierarchy) or the **data input** (importance sliders and dates).

- **Ratz’s Tip**: If you find that the priorities seem off, use the **reset all tasks to normal urgency and importance** button and start over. This can help clear any confusion caused by previous incorrect adjustments.

---

### **Final Example of a Proper Setup:**

Let’s take a project called **"Plan a Conference"**. Here’s how you would apply **Ratz’s Computed-Score Priority system** step-by-step:

1. **Parent Task**: Plan a Conference
   - **Importance Slider**: Set based on how important this task is compared to other parent tasks (e.g., "Write a Research Paper").
   - **Due Date**: The date by which the conference must be planned.

2. **Subtasks**:
   - **Subtask 1**: Book Venue
     - **Importance Slider**: High importance because it’s crucial to planning the conference.
     - **Start Date**: Set for when you need to start looking for venues.
     - **Due Date**: Set for when the venue needs to be booked.
  
   - **Subtask 2**: Send Invitations
     - **Importance Slider**: Medium importance because it’s important but not as critical as booking the venue.
     - **Start Date**: Set for when you need to start sending invitations.
     - **Due Date**: Set for when invitations must be sent.

3. **Adjust Preferences**:
   - Set **moderate weighting factors** for start and due dates to control urgency.
  
4. **Let MLO Calculate the Priority**:
   - MLO will combine the importance and urgency values to generate a **To-Do List** with the most critical tasks at the top.

---

### **Conclusion:**
By following this step-by-step setup, and remembering to **only set importance for tasks with siblings**, you can leverage **Ratz’s Computed-Score Priority system** to manage tasks based on **importance** and **urgency** in a natural and controlled way. This approach avoids artificial urgency boosts and ensures that your task list reflects the true priorities of your work, without over-complicating the task hierarchy.