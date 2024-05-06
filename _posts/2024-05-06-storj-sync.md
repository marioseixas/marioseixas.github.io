---
categories:
  - Tutorial
  - Code
tags:
  - linux
  - scripts
comment: 'https://rclone.org/s3/#storj'
info: aberto.
date: '2024-05-06'
type: post
layout: post
published: true
slug: storj-sync
title: 'Rclone: syncing local and STORJ cloud'
mermaid: true
---

### 1. Synchronize Root-Level Files

For synchronizing files directly under `/userdata` (excluding subdirectories), use the following command:

```bash
rclone sync /userdata/ Storj:transfer/999_SHARED --exclude '**/' --progress
```

### 2. Dynamic Subfolder Synchronization Script

To ensure subfolders are accurately synchronized to the corresponding subfolders under `999_SHARED`, and to incorporate error handling, use this script:

```bash
#!/bin/bash

for dir in /userdata/*/; do
    dirname=$(basename "$dir")
    # Sync each subdirectory to the corresponding subdirectory under 999_SHARED
    rclone sync "$dir" Storj:transfer/999_SHARED/"$dirname" --progress 2>>/var/log/rclone_errors.log
    if [ $? -eq 0 ]; then
        echo "Successfully synced $dirname" | tee -a /var/log/rclone_sync.log
    else
        echo "Error syncing $dirname. Check /var/log/rclone_errors.log for details." | tee -a /var/log/rclone_sync.log
    fi
done
```

### 3. Automation with Cron

For regular updates, automate the synchronization process through a cron job:

```bash
crontab -e
```

Add the following entries to execute the synchronization daily at 1 AM:

```cron
0 1 * * * rclone sync /userdata/ Storj:transfer/999_SHARED --exclude '**/' --progress >> /var/log/rclone_sync.log 2>&1
1 1 * * * /path/to/sync_script.sh
```
