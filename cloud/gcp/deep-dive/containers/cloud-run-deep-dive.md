# Cloud Run Deep Dive

### Topic 1: Foundations – The "Serverless Container"

To understand Cloud Run, we have to look at the landscape of compute before it arrived. We had two extremes:

1. **Cloud Functions (Function-as-a-Service):** You give us code (Python, Node, Go). We run it.
   * *Pros:* Zero ops, scales to zero.
   * *Cons:* You are locked into specific runtimes/versions. You cannot install arbitrary system binaries (e.g., ImageMagick or a specific PDF generator). Local testing is often "mocked" rather than identical to production.


2. **Google Kubernetes Engine (GKE):** You give us containers. We run them on a cluster.
   * *Pros:* Ultimate control. Any binary, any language.
   * *Cons:* You manage the cluster (or at least the configuration of it). You pay for the nodes even if no traffic is hitting them (unless you tune autoscaling aggressively, which is slow).


#### The "Sweet Spot": Cloud Run

Cloud Run bridges this gap using the **Serverless Container** model.

**The "Contract"**
Cloud Run doesn't care what language you write in. It doesn't care if you use Python, Rust, Java, or a bash script. It only cares about a specific **contract**:

1. **The Artifact:** You must package your application as a container image (OCI standard).
2. **The Listener:** Your container must start an HTTP server and listen on the port defined by the environment variable `$PORT` (default is 8080).
3. **Statelessness:** You must assume that any file you write to disk or any data stored in memory could disappear instantly after a request finishes.
4. **Fast Startup:** The platform expects your container to boot up and listen for requests within milliseconds (or very few seconds), or it will time out.

#### The Knative Heritage

Google didn't just build a proprietary black box. They open-sourced the API specification for serverless containers as **Knative**.

Cloud Run is essentially **Google's managed implementation of Knative Serving**.

* This means if you write a YAML file to deploy to Cloud Run, that same YAML (mostly) works on a GKE cluster with Knative installed, or on OpenShift, or on AWS with Knative.
* It prevents "Vendor Lock-in" at the API level.

#### Visualizing the Hierarchy

Here is how the abstraction layers stack up:

```text
       +-----------------------------------------+
       |               Cloud Functions           |  <-- Code only.
       |        (Restricted environment)         |      High constraints.
       +-----------------------------------------+

       +-----------------------------------------+
       |               CLOUD RUN                 |  <-- "The Sweet Spot"
       |     (Container + HTTP listener)         |      Any binary + Serverless ops.
       +-----------------------------------------+

       +-----------------------------------------+
       |               KUBERNETES (GKE)          |  <-- Orchestration.
       |     (Pods, Deployments, Services)       |      High Control / High Ops.
       +-----------------------------------------+

       +-----------------------------------------+
       |          COMPUTE ENGINE (VMs)           |  <-- Raw Infrastructure.
       |        (OS, Kernel, Networking)         |      Full Ops.
       +-----------------------------------------+

```

#### Mental Lab: Scenario 1

**The Scenario:**
You have a legacy data processing script written in **Fortran** that processes weather data. It relies on an obscure, 10-year-old Linux system library (`lib-obscure.so`) that is not present in standard modern operating systems. You want this script to run only when a user uploads a file, and you don't want to pay for a server running 24/7.

**The Question:**

1. Why would **Cloud Functions** likely fail for this scenario?
2. Why is **Cloud Run** a better fit here than **GKE**, given the requirement "don't want to pay for a server running 24/7"?

#### Answer Key: Mental Lab 1

**1. Why Cloud Functions fails:**

* **Runtime Limitations:** Cloud Functions typically supports specific languages (Node.js, Python, Go, Java, etc.). It does not natively support **Fortran**.
* **System Dependencies:** Installing a custom system library (`lib-obscure.so`) is difficult or impossible in the standard Cloud Functions environment because you don't control the OS image or the build process of the underlying container as fully as you do with Docker.

**2. Why Cloud Run beats GKE here:**

* **Cost (Scale-to-Zero):** In standard GKE, you have to pay for the "Nodes" (VMs) that make up the cluster, even if they are sitting idle at 3:00 AM waiting for a file upload.
* **Management:** With Cloud Run, you don't manage a cluster master, node pools, or upgrades. You just give Google the container. If no one uploads a file for a week, your bill is **$0.00**.

---

### Topic 2: Core Components

In Cloud Run, the hierarchy is strict. It flows like this: **Service -> Revision -> Instance**.

#### 1. The Service

The **Service** is the main resource you manage.

* It provides the **stable endpoint** (e.g., `https://weather-app-xyz.a.run.app`).
* It acts as the "Traffic Controller." It decides which version of your code receives the traffic coming to that URL.
* It holds the configuration for IAM (who can call this service?) and custom domains.

#### 2. The Revision (Crucial Concept)

Every time you deploy to a Service, Cloud Run creates a **Revision**.

* **Immutability:** A Revision is **immutable**. Once created, it cannot be changed. If you want to change an environment variable or update the container image, you *must* create a new Revision.
* **Snapshot:** Think of a Revision as a "Time Capsule" containing:
1. The specific Container Image Digest.
2. The Environment Variables at that moment.
3. The Resource limits (CPU/RAM).


* **Rollbacks:** Because Revisions never change, "rolling back" is instantaneous. You just tell the Service: "Point traffic back to Revision 1."

#### 3. The Instance

The **Instance** is the actual invisible worker.

* It is a micro-VM (more on this later) running your container.
* Instances are **ephemeral**. They are created when traffic arrives and destroyed when traffic stops.
* You do not manage Instances directly (you can't SSH into them). You manage the *rules* for how they scale.

#### 4. Cloud Run Jobs (The Sibling)

Briefly, there is a sibling to the Service called a **Job**.

* **Service:** Listens for HTTP requests. Runs indefinitely (as long as requests come).
* **Job:** Does a task and quits. It does *not* listen on a port. Useful for database migrations or batch processing.

#### Visualizing the Architecture

Imagine a "Traffic Split" scenario where you are testing a new version.

```text
       USER REQUEST (Internet)
              |
              v
    +-----------------------+
    |    CLOUD RUN SERVICE  |  <-- The Stable URL
    |  (Traffic Controller) |
    +----------+------------+
               |
               | Traffic Split Rule:
               | "90% to Rev-1, 10% to Rev-2"
               |
      +--------+------------------+
      |                           |
      v                           v
+--------------+           +--------------+
|  REVISION 1  |           |  REVISION 2  |  <-- Immutable Snapshots
|  (Stable)    |           |  (Canary)    |
+------+-------+           +------+-------+
       |                          |
       | Autoscales               | Autoscales
       v                          v
 [Instance] [Instance]      [Instance]

```

####  Mental Lab: Scenario 2

**The Scenario:**
You have a Cloud Run Service named `payment-processor`. It is currently running **Revision A**, which connects to a database using the environment variable `DB_HOST=10.0.0.1`.

You realize the IP is wrong. It should be `10.0.0.5`.

You run a command to update the environment variable to `10.0.0.5`.

**The Question:**

1. Does **Revision A** get updated with the new IP?
2. What happens to the requests currently being processed by the instances of **Revision A** the moment you hit "update"? Do they crash?

#### Answer Key: Mental Lab 2

**1. Does Revision A get updated?**

* **No.** Revisions are strictly **immutable**. The moment you hit "update", Cloud Run creates a brand new **Revision B** with the new IP address. Revision A remains frozen in time with the old IP.

**2. What happens to requests currently on Revision A?**

* **They finish gracefully.** This is a key feature of Cloud Run. The platform performs a generic "Blue/Green" deployment automatically.
* New traffic starts flowing to Revision B immediately (or gradually, if you configured traffic splitting).
* Existing connections on Revision A are allowed to complete their work. Revision A will only spin down (scale to zero) once those active requests are done.

---

### Topic 3: The Request Lifecycle

This is where the magic happens. How does a request get from a user's laptop to your specific container buried deep in a Google data center?

We will trace a request hitting `https://myservice-xyz.a.run.app`.

#### Step 1: The Global Edge (Google Front End)

When a user makes a request, they are not connecting directly to the server in the data center.

* **Anycast IP:** The DNS for `*.run.app` resolves to a global Anycast IP address. This means the user connects to the **closest Google Point of Presence (PoP)** geographically.
* **The GFE (Google Front End):** This is Google's massive reverse proxy system.
* **SSL Termination:** The TLS (HTTPS) handshake happens here, at the edge, close to the user. This makes the connection fast.
* **DDoS Protection:** The GFE filters out malicious volumetric attacks before they ever reach your region.



#### Step 2: The Private Backbone

Once the GFE accepts the request, it doesn't send it back out to the dirty public internet. It sends it onto **Google's Private Network Backbone**.

* This is a dedicated fiber optic network connecting Google's data centers globally. It is faster and more reliable than the public internet.

#### Step 3: The Regional Router & The "Activator"

The request arrives at the specific Google Cloud Region where you deployed (e.g., `us-central1`).

* **Routing:** The internal load balancer looks up your Service.
* **The "Activator" Check:**
  * *Scenario A (Warm):* If instances are already running, the request is passed directly to one of them.
  * *Scenario B (Cold):* If your service is scaled to zero, the request hits a component called the **Activator**. The Activator **holds the request in a queue** (up to 10 seconds usually). It signals the infrastructure to boot up a new Instance. Once the instance says "I'm ready," the Activator releases the queued request to it.



#### Step 4: The Instance (gVisor)

The request reaches your Instance.

* **The Sandbox:** Your container is not running on a standard Linux kernel shared with other customers. It is running inside **gVisor**.
* *gVisor* is a user-space kernel (written in Go) that intercepts system calls. It acts as a heavy security buffer. Even if malware escapes your container, it is trapped in the gVisor sandbox and cannot touch the host node or other neighbors.


* **The Contract:** The request hits your application on `localhost:$PORT`.

#### Visualizing the Lifecycle

```text
       User (Laptop in London)
             |
             v  <-- 1. Latency is low (connects to London Edge)
      +--------------+
      |  Google Edge |  <-- SSL Decryption happens here
      |     (GFE)    |
      +------+-------+
             |
             |  <-- 2. Travels fast over Google Private Fiber
             |         (London -> Iowa)
             v
      +--------------+
      | Region (Iowa)|
      |   Router     |
      +------+-------+
             |
             v  <-- 3. Is there an instance?
     +-------+-------+
     |               |
   (Yes)           (No) -> Hit "Activator" -> Queue -> Boot Instance
     |               |
     v               v
+----------+   +----------+
| Instance |   | Instance |  <-- 4. Running inside gVisor Sandbox
+----------+   +----------+

```

#### Mental Lab: Scenario 3

**The Scenario:**
You have a Cloud Run service deployed in **`us-central1` (Iowa, USA)**.
A user in **`asia-northeast1` (Tokyo, Japan)** makes an HTTPS request to your service.

**The Questions:**

1. Where does the **TCP/TLS Handshake** take place? (Tokyo or Iowa?)
2. If your service is currently scaled to zero, the user experiences a "Cold Start" delay (e.g., 2 seconds). During those 2 seconds, is the HTTP request dropped/failed, or is it waiting somewhere? If waiting, where?

#### Answer Key: Mental Lab 3

**1. Where does the TCP/TLS Handshake take place?**

* **Tokyo (Japan).** This is a critical performance win. The user's device connects to the nearest Google Edge Point of Presence (PoP) in Tokyo. The expensive "round trips" required to negotiate encryption (the handshake) happen over a short distance (User <-> Tokyo). Once the secure tunnel is established, the data rides Google's high-speed private fiber to Iowa. If the handshake had to go all the way to Iowa, the latency would be noticeably higher.

**2. Where is the request waiting during a Cold Start?**

* **The Activator Queue.** The request is **not dropped**. It is held in a pending state by the Cloud Run infrastructure (specifically the "Activator" component we discussed) for up to ~10 seconds. The user's browser sees a "loading" spinner. Once the new container instance signals "Ready," the request is released from the queue and processed.

---

### Topic 4: Scaling Mechanics

You now understand *how* a request gets there. Now we need to understand *how many* containers handle those requests. This is where Cloud Run differs drastically from standard Kubernetes or older "Functions" models.

#### 1. The "Concurrency" Superpower

Most Function-as-a-Service (FaaS) platforms (like AWS Lambda historically) use a **1:1 model**. One request = One container instance. If 100 people hit your site at once, the platform spins up 100 instances. This is expensive and leads to many cold starts.

Cloud Run is different. It supports **Concurrency**.

* **Definition:** Concurrency is the maximum number of requests a *single* container instance can handle simultaneously.
* **Default:** 80.
* **Maximum:** 1000.

**How it works:**
If your concurrency is set to **80** and you have **50** concurrent users, Cloud Run spins up **1 instance**.
If you have **100** concurrent users, Cloud Run spins up **2 instances** (80 on the first, 20 on the second).

**Why is this huge?**

* **Fewer Cold Starts:** One container can absorb a traffic spike (up to its limit) without needing to wait for a new container to boot.
* **Shared Resources:** If your app connects to a database, 100 requests sharing one container means **1 database connection**. In the 1:1 model, that would be 100 database connections (DDoS-ing your own database).

#### 2. Scale-to-Zero vs. Min Instances

* **Scale-to-Zero:** If no requests come in, Cloud Run kills the last instance. You pay $0.
* *Trade-off:* The next user faces a "Cold Start."


* **Min Instances:** You can set "Min Instances = 1" (or more).
* *Trade-off:* You pay for that 1 instance 24/7, even if it's idle.
* *Benefit:* The "Activator" never has to queue a request for booting; there is always a warm instance ready.


#### 3. The CPU Allocation Models (The Billing Trap)

Cloud Run offers two very different ways to pay and use CPU. This is often misunderstood.

**A. CPU only allocated during request processing (Default)**

* **Behavior:** When a request comes in, your CPU powers up. When the request finishes (returns the response), the CPU is **throttled to nearly zero**.
* **Implication:** You *cannot* run background threads (like a polling loop or processing a queue after returning an HTTP 200) because the CPU literally pauses.
* **Billing:** You only pay when a request is active.

**B. CPU always allocated**

* **Behavior:** The CPU behaves like a standard server. It runs 100% of the time as long as the instance is alive.
* **Implication:** You *can* run background tasks.
* **Billing:** You pay for the entire lifecycle of the instance (from boot to shutdown), regardless of traffic.


#### Mental Lab: Scenario 4

This is a capacity planning puzzle.

**The Scenario:**
You have a high-traffic "Flash Sale" service.

* **Average Request Duration:** 200ms (0.2 seconds).
* **Concurrency Setting:** 10.
* **Traffic Spike:** You are receiving **500 requests per second**.

**The Question:**
Approximately how many container instances does Cloud Run need to spin up to handle this load?

*Hint: Calculate how many requests one instance can handle in one second (throughput), then divide the total load by that number.*

#### Answer Key: Mental Lab 4

**The Answer: 10 Instances.**

**The Math:**

1. **Throughput per "Slot":** If a request takes **200ms** (0.2s), one "concurrency slot" can handle **5 requests per second** (1 sec / 0.2 sec = 5).
2. **Throughput per Instance:** Your instance has **10 slots** (Concurrency = 10).
   * $10 \text{ slots} \times 5 \text{ req/s} = 50 \text{ requests per second per instance}$.


3. **Total Instances Needed:**
   * $500 \text{ total req/s} / 50 \text{ req/s per instance} = 10 \text{ instances}$.

**Why this matters:**
If you were using a standard Function-as-a-Service (Concurrency = 1), you would need **100 instances** to handle the same load.

* **Cloud Run:** 10 Cold Starts.
* **Standard FaaS:** 100 Cold Starts.
* **Result:** Cloud Run is 10x more efficient here.

---

### Topic 5: Networking & Security

We now have a scalable service. But currently, it lives on the public internet. Most enterprise apps need to talk to private databases (Cloud SQL, Redis) and block public access.

This brings us to **Ingress** (Incoming) and **Egress** (Outgoing).

#### 1. Ingress Control ("Who can call me?")

By default, a Cloud Run service url (`*.run.app`) is public. You can lock this down.

* **"All":** Public internet access.
* **"Internal":** Only callable from:
  * VPC networks in the same project/perimeter.
  * Other Cloud Run services.
  * **Crucially:** An **Application Load Balancer (ALB)**.


* **"Internal and Cloud Load Balancing":** Similar to above, but explicitly allows the ALB.

**Why use an ALB?**
If you want WAF (Web Application Firewall) protection (Cloud Armor) or custom domain routing, you put an ALB in front and set Cloud Run Ingress to "Internal". This forces all traffic through your security checkpoint.

#### 2. Egress Control ("Who can I call?")

By default, your container can *only* see the public internet. It **cannot** see your private Cloud SQL instance on `10.0.0.5`.

To fix this, we need to bridge the "Serverless World" with your "VPC World".

**Option A: Serverless VPC Access Connector (The "Old" Way)**

* You provision a "Connector" resource.
* Under the hood, Google spins up hidden VM instances that act as a NAT/Bridge.
* *Pros:* Static IP support.
* *Cons:* You pay for those bridge VMs 24/7, even if your Cloud Run service scales to zero. It limits throughput.

**Option B: Direct VPC Egress (The "New" Way)**

* You attach your Service directly to a VPC Subnet.
* *How it works:* Google attaches a virtual network interface (NIC) to your micro-VM instance directly inside your VPC.
* *Pros:* Faster, cheaper (no bridge VMs), no bottleneck.
* *Cons:* Uses up IP addresses in your subnet rapidly as you scale.

#### 3. Service Identity (IAM)

Every Cloud Run revision runs as a specific **Service Account**.

* **Default:** Default Compute Engine Service Account (Too permissive! Has Editor access).
* **Best Practice:** Create a dedicated Service Account (e.g., `payment-service-sa@...`).
* Grant it *only* the permissions it needs (e.g., `cloudsql.client`, `pubsub.publisher`).
* If your code gets hacked, the attacker can only do what that specific Service Account allows.


####  Mental Lab: Scenario 5 (The Final Boss)

This scenario combines everything we have learned: Scaling, Networking, and Security.

**The Scenario:**
You are building a sensitive "Employee Payroll" API.

1. **Database:** A private Cloud SQL instance (IP: `172.16.0.5`). It has **no public IP**.
2. **Access:** The API must **not** be accessible from the public internet. It should only be callable by your internal legacy VM application running in the same VPC.
3. **Cost:** The API is used only once a month (Payroll day). You want costs to be near zero for the rest of the month.

**The Configuration Challenge:**
Please specify the settings for these three areas:

1. **Ingress Setting:** (All / Internal / Internal + LB?)
2. **Egress Setting:** (None / Direct VPC Egress / Public?)
3. **Authentication:** How does the legacy VM prove to Cloud Run that it is allowed to call the Payroll API? (Hint: It involves IAM).

#### Answer Key: Mental Lab 5

**1. Ingress Setting: `Internal**`

* **Why:** You selected "Internal" (or "Internal and Cloud Load Balancing" if you had a load balancer, but here we don't need one).
* **The Effect:** This immediately blocks any request coming from the public internet. If a hacker tries to `curl https://payroll-api...`, they get a **403 Forbidden**.
* **The Access:** It allows requests *only* from within the VPC (your legacy VM) or other Google Cloud services in the same project.

**2. Egress Setting: `Direct VPC Egress**`

* **Why:** Your database is on a private IP (`172.16.0.5`). By default, Cloud Run cannot see private IPs.
* **The Mechanism:** You attach the Cloud Run service to the specific VPC Subnet where the database lives (or a peered one).
* **The Cost Win:** Unlike the older "VPC Access Connector" which requires keeping a VM running 24/7 (costing money even when idle), **Direct VPC Egress** has no fixed cost. You only pay for the data transfer during the payroll run. When the job finishes, costs drop to near zero.

**3. Authentication: IAM OIDC Tokens**

* **The Mechanism:** The legacy VM cannot just "be trusted" because it's on the network. It needs an identity.
1. The VM has its own **Service Account**.
2. The VM queries the local Metadata Server (`http://metadata...`) to get an **OpenID Connect (OIDC) ID Token**.
3. The VM sends the request to Cloud Run with the header: `Authorization: Bearer <ID_TOKEN>`.


* **The Check:** Cloud Run validates the token. If the VM's Service Account has the IAM role **"Cloud Run Invoker"** on the Payroll Service, the request is allowed. If not, **403 Forbidden**.

#### Visualizing the Secure Architecture

```text
       Legacy VM (Employee Portal)
       [Service Account: vm-sa@...]
              |
              | 1. Request ID Token from Metadata Server
              | 2. Send HTTP POST with Auth Header
              v
      +-----------------------+
      |  CLOUD RUN SERVICE    |  <-- Ingress: Internal Only
      |    (Payroll API)      |      Auth: Requires "Invoker" Role
      +----------+------------+
                 |
                 | 3. Traffic leaves via Direct VPC Egress
                 |
                 v
         (VPC Network)
                 |
                 v
      +-----------------------+
      |    CLOUD SQL (DB)     |  <-- Private IP: 172.16.0.5
      |   (Payroll Data)      |
      +-----------------------+

```

---

