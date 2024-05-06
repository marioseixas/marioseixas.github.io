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
title: 'Rclone: Syncing STORJ Cloud to Local Storage'
mermaid: true
---

### 1. Synchronize Root-Level Files
To synchronize files from the STORJ cloud (`999_SHARED`) to a local directory (`/userdata`), excluding subdirectories, use the following command:
```bash
rclone sync Storj:transfer/999_SHARED/ /userdata/ --exclude '**/' --progress
```
This command ensures that only the files at the root of `999_SHARED` are synchronized, without recursing into subdirectories.

### 2. Dynamic Subfolder Synchronization Script
To ensure that each subfolder in `999_SHARED` on STORJ is synchronized to the corresponding local subfolder under `/userdata`, and to include error handling, use the following script:
```bash
#!/bin/bash
# Listing directories in Storj:transfer/999_SHARED/
directories=$(rclone lsd Storj:transfer/999_SHARED/ --format p | awk '{print $NF}')

for dir in $directories; do
    # Ensure the directory exists locally
    mkdir -p "/userdata/$dir"
    # Sync each subdirectory from STORJ to local
    rclone sync "Storj:transfer/999_SHARED/$dir" "/userdata/$dir" --progress 2>>/var/log/rclone_errors.log
    if [ $? -eq 0 ]; then
        echo "Successfully synced $dir" | tee -a /var/log/rclone_sync.log
    else
        echo "Error syncing $dir. Check /var/log/rclone_errors.log for details." | tee -a /var/log/rclone_sync.log
    fi
done
```
This script first fetches the list of directories under `999_SHARED`, ensures these directories exist locally, and then synchronizes each one. It logs errors to `/var/log/rclone_errors.log` and writes both successful and unsuccessful sync messages to `/var/log/rclone_sync.log`.

### 3. Automation with Cron
For regular updates, you can automate the synchronization process through a cron job:
```bash
crontab -e
```
Add the following entries to execute the synchronization daily at 1 AM:
```
0 1 * * * rclone sync Storj:transfer/999_SHARED /userdata --exclude '**/' --progress >> /var/log/rclone_sync.log 2>&1
1 1 * * * /path/to/sync_script.sh
```
