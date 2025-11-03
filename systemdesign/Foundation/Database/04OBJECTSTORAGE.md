## 📦 Object Storage

Object storage is a data storage architecture that manages data as **objects**, distinct from the hierarchical files and folders of file storage (like an SSD or hard drive) or the tables and rows of a relational database.

### 1. The Core Concept: Objects and Buckets

In object storage, the basic unit is an **object**, which is stored inside a flat structure called a **bucket**.

* **The Object:** An object bundles three things together:
    1.  **The Data Itself:** An unstructured stream of bytes (e.g., a photo, a video file, a backup image, a document).
    2.  **Metadata:** A set of attributes that describe the data (e.g., creation date, file type, file size, permissions, owner, etc.). This can be system-defined or custom user-defined data.
    3.  **A Globally Unique Identifier (Key):** A simple name or key used to retrieve the object. This is often a path-like string (e.g., `images/users/user_123/profile.jpg`), but the storage system treats the structure as flat.

* **The Bucket:** This is the top-level container for objects. It has a globally unique name (e.g., `my-company-product-images`). Buckets define high-level access policies, geographical regions, and billing rules.

### 2. How It Differs Architecturally

Object storage is designed from the ground up to address the limitations of traditional storage models when dealing with massive scale.

| Feature | Object Storage (e.g., AWS S3, Google Cloud Storage) | File Storage (e.g., NAS, Local Disk) |
| :--- | :--- | :--- |
| **Structure** | **Flat structure** (no folders, just buckets and keys). | Hierarchical (folders, sub-folders, drives). |
| **Access Protocol** | **HTTP/S (REST API)**—Accessed via URLs. | Block-level (OS kernel) or File-level (NFS/SMB). |
| **Scalability** | **Massively Horizontal** (virtually limitless scale). | Vertical, limited by the size of the server/array. |
| **Data Retrieval** | Access by Key (URL). | Access by File Name and File Path. |
| **Integrity** | Focuses on **Durability** (often 99.999999999% durability). | Focuses on speed and transactional throughput. |

### 3. Key Design Properties

Object storage excels because it prioritizes three main characteristics, often at the expense of transactional speed:

#### A. Massive Scalability and Availability
Object storage is built on a distributed cluster of commodity hardware.

* **Mechanism:** When you store an object, the system automatically **replicates** it across multiple physical disks, availability zones, and even geographic regions.
* **Result:** This provides extreme **availability** (zero single point of failure) and **scalability**. There is no practical limit to the number of objects you can store.

#### B. Durability
This is arguably the defining feature of object storage, often quoted as "eleven nines" of durability.

* **Mechanism:** Durability is achieved through **erasure coding** and redundancy. Data is broken up into fragments, encoded with parity data, and spread across many disks. Even if multiple disks fail, the original object can be mathematically rebuilt.
* **Result:** Data loss is extremely unlikely.

#### C. Simplicity (RESTful API)
Objects are accessed using standard web protocols.

* **Mechanism:** Access is done via a **REST API** using four basic operations:
    * **PUT:** Upload a new object (e.g., `PUT /my-bucket/image.jpg`).
    * **GET:** Retrieve an object (e.g., `GET /my-bucket/image.jpg`).
    * **DELETE:** Remove an object.
    * **POST/List:** Create a bucket or list the keys within a bucket.
* **Result:** This simplicity allows any HTTP-capable application, website, or mobile device to interact with the storage directly.

### 4. Ideal Use Cases in System Design 🎯

In a system design context, object storage is typically used for things that don't change often and need to be accessible globally at massive scale.

* **Static Assets/Media:** Storing images, videos, audio files, and scripts for websites and applications (often served via a CDN like CloudFront). **This offloads load from the main application servers.**
* **Data Lakes & Big Data:** Storing massive amounts of raw, unstructured data (logs, IoT sensor data, historical archives) to be processed by big data tools like Spark or Hadoop.
* **Backups and Archiving:** Long-term, highly durable storage for disaster recovery, as it is cheaper and more resilient than block storage.
* **User-Generated Content (UGC):** Storing files uploaded by users, such as profile photos, documents, and videos.

### Example: Storing a User's Profile Picture

Imagine you are designing the system for a social media platform:

1.  The user uploads `profile.jpg` from their mobile app.
2.  The application server generates a unique key, such as `user_uploads/profiles/user_456/v1/profile_original.jpg`.
3.  The application sends the file and the key to the **Object Storage** service (e.g., S3).
4.  The object is saved, replicated, and is now accessible via a unique URL: `https://my-social-bucket.s3.aws.com/user_uploads/profiles/user_456/v1/profile_original.jpg`.
5.  The application's **SQL Database** only stores the URL string, **not** the image data itself. This keeps the transactional database lean and fast.