# Assignment Overview

This assignment is divided into two activities:

---

## Activity 2.1: Deduplication

### Dataset
- **File**: `dedup_data.csv`
- **Size**: ~5,000 entries
- **Content**: Synthetically generated person records

### Data Fields
Each entry contains the following details:
- `id` (unique identifier)
- `given_name`
- `surname`
- `street_number`
- `address_1`
- `address_2`
- `suburb`
- `postcode`
- `state`
- `date_of_birth`
- `soc_sec_id`

### Task
Identify and group all records belonging to the same person. Multiple entries may exist for each person with variations due to reporting noise and errors.

---

## Activity 2.2: Crawling

### Overview
You are provided with a web server that can be run locally. The server returns pages containing:
- **`page_id`**: Unique identifier for the page
- **`node_id`**: Updates at unknown time intervals
- **Node history**: All previous node IDs and update timestamps
- **Outgoing links**: List of all links from that page

### Task
1. Crawl the website
2. Estimate the PageRank of each page
3. Track updated node IDs for all pages
4. **Minimize the number of page visits** (efficiency is key)

### Development Status
- Incremental updates to the web server will be rolled out
- Instructions will be provided as updates are released
- A test Docker image (`.tar` file for AMD64 systems) is attached
- Server runs on **port 3000**
- **Note**: This is not the final version and may contain bugs
- Report issues to TAs via the Moodle announcement thread

---

## Running the Web Server

### Prerequisites
- Docker installed on your system
- AMD64 architecture

### Commands

#### 1. Verify Image Contents (Optional, but Recommended)
```bash
sha256sum -c crawling_assignment-1.0-amd64.tar.sha256
```

#### 2. Load the Docker Image (One-Time Operation)
```bash
docker load -i crawling_assignment-1.0-amd64.tar
```

#### 3. Run the Server (Each Time You Restart)
```bash
docker run --rm -p 3000:3000 --read-only --tmpfs /tmp:rw,noexec,nosuid --cap-drop ALL --security-opt no-new-privileges --pids-limit 128 --memory 256m crawling_assignment:1.0
```

### Server Access
Once running, the web server will be available at:
```
http://localhost:3000
```

---