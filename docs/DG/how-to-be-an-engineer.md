---
doc_uid: "MOS-ENG-DG-001"
title: "How to Be an Engineer"
org: "MOS"
category: "DG"
department: "ENG"
notion:
  database: "Documents"
  publish: true
access_groups:
  - "All-Hands"
lifecycle:
  desired_state: "draft"
---
# How to Be an Engineer

*A collection of engineering wisdom from Mosaic Design Labs*

---

Engineering is fundamentally the art of managing trade-offs—taking a problem-solving approach where we use the tools of science and technology to invent solutions to real-world problems. What follows is a set of principles we've developed over years of building biomedical instruments, diagnostic devices, and embedded systems. Some of these ideas are timeless. Others reflect what we think matters most in an era where AI is reshaping how engineers work.

---

## 1. Focus on Fundamentals

Develop a deep understanding of the core principles behind the technologies you work with. Understand their fundamental trade-offs. Build a working knowledge of what we call **settled technology**—best practices and platforms that have been validated by the industry and that you probably don't need to revisit.

Settled technology includes things like the ARM microcontroller architecture, which has become the dominant platform for embedded systems. It includes System-on-Modules (SOMs) like the Raspberry Pi Compute Module, which let you drop embedded Linux into virtually any product from day one without spending engineering hours on 12-layer PCB layouts, differential signaling, or Wi-Fi certifications. It includes injection molding as the preferred fabrication method for high-volume parts. Unless you have a compelling reason to deviate from settled technology, don't. You'll be more efficient building on what has already been demonstrated.

On the physics side, work to develop intuition around fundamental trade-offs: sensitivity versus specificity in instrumentation, sensitivity versus speed, cost versus performance. Develop intuition around tolerances—what's reasonable for a machined part versus an injection-molded part versus a 3D-printed part. When you design mechanical assemblies, be mindful of where your critical-to-quality (CTQ) attributes lie, and work to minimize the number of tight tolerances needed to achieve the desired operating characteristics of the system.

Finally, understand what manufacturing approaches are available to you. Get hands-on experience—whether in a prototyping lab or by working with a vendor and asking lots of good questions.

## 2. Think at the Systems Level

Especially now, when AI tools let us go deep into particular topics very quickly, it's more important than ever to see the bigger picture of an engineered system and how its subsystems fit together.

In hardware development—particularly hardware that intersects with biology and medicine—"the system" doesn't stop at the electromechanical hardware interacting with firmware interacting with a cloud database. It extends to how that hardware interacts with tissue, molecular biology, a healthcare system, and the practice of healthcare itself. The future of engineering involves tighter coupling between those who understand the problems and those who understand the potential solutions. The more you can be both—the more you can have those conversations within yourself and your engineering team—the more successful you will be.

Systems thinking also exposes trade-offs that aren't apparent to an engineer focused only on a PCB or a cartridge. There are often ways of solving problems between hardware and software, or ways of shifting how technology is applied in practice that make better or lower-cost solutions possible.

## 3. Consult Experts

One hour with somebody who has deep experience in the technical area you're working on can save you years and millions of dollars. This is not an exaggeration.

Think of your development journey as a tree of possibilities branching out from the present moment and your current understanding of the problem. The better you understand the problem, the more likely those branches lead to success. Expert guidance helps you prune entire branches of unproductive technical development before you invest in them. Seek out people who have been there and done that, and listen carefully.

## 4. Define the Problem, Then Define the Solution

Too often, engineers just want to start building. But particularly when you're working with a client who has a specific budget and objective, it's critical to align on what problem you're solving and what criteria you'll use to know you've solved it. Only then should you define solutions.

Very often clients come with a solution in mind and just want you to build it. It can be difficult to back up and have the conversation about the problem. But defining the problem can take as much effort as creating the solution. It means talking to customers, finding customers willing to talk, and aggregating messy customer discovery information into a coherent problem statement.

One of the best frameworks for this process is Stanford's **Biodesign** curriculum. Define the problem, be clear about the value proposition and who it's intended for, and begin writing down requirements—understanding that they will evolve as your understanding of customers and users deepens. The more you can write down requirements and specifications, the more you bring everyone to the same page and ensure you're working toward a common vision of success.

## 5. Plan to Iterate, and Iterate the Plan

Prototyping is about iteration. Early in a project, outline a **prototype roadmap** that defines what you want to build and why at each stage. This promotes productive conversations around questions like: What are our biggest risks, and how do we de-risk them early? What prototyping methods get us results quickly and cheaply? What is each prototype round designed to teach us?

Then follow through. At every cycle, review what you learned and set yourself up for the next cycle so those learnings carry forward. The plan itself should evolve as you learn.

## 6. Use Off-the-Shelf Components

Don't reinvent the wheel unless there's a compelling reason. The advent of SOMs and compute modules has allowed us to drop embedded Linux into virtually any product from the beginning and maintain that architecture through the entire development lifecycle. We don't have to spend time on problems that have already been solved. This lets us focus on the core technology at hand.

The same principle applies across domains: use proven libraries, established communication protocols, standard connectors, and validated components wherever possible. Save your engineering energy for the problems that actually require invention.

## 7. Always Consider Cost

Even in early prototyping—where cost is less of a concern because you're maximizing learning—you need to maintain line of sight to a manufacturable product that meets the customer's cost targets. This is a fundamental difference between scientists and engineers. Engineers should always be thinking about cost.

## 8. Study How Things Are Made

Take products apart. You can learn an enormous amount from products adjacent to the one you're building. You may even find products essentially identical to yours. Take them apart. Understand the design decisions that were made. Get in the designer's head: Why did they put this shielding here? Why machine this part rather than injection-mold it? Why separate these PCBs? How did they ensure optical alignment? How was this assembled?

By taking it apart and reassembling it, you'll find ways the product could be improved. Products that go to market are rarely perfect. If your goal is to build a better version of an existing instrument, start by studying the ones that have succeeded. You can find used equipment on eBay and auction sites for very little money. There's no excuse not to do it, and it's fun.

## 9. Be Data-Driven and Model-Driven

If you can develop a model—whether it's a finite element simulation in COMSOL, a ray-tracing model in Zemax, a SPICE circuit simulation, or even a back-of-the-envelope calculation—use it to guide decision-making around geometries, sensitivities, tolerances, and resolution. With today's AI tools, there's no excuse not to do at least some level of analytical estimation, even if you're not formally trained in the relevant discipline.

But ultimately, one well-designed experimental result is worth a thousand models. Emphasis on *well-designed*. Too often engineers run inconclusive experiments, ignore statistical significance, and make important decisions based on an N of 1. Know your statistics and apply them rigorously.

Data-driven decision-making is also critical for managing disagreements on a team. If you can orient everyone around an A/B test of two approaches, it takes the ego out of the discussion. Everyone responds to data. And don't be afraid to critique the data if you think the experiment is flawed.

## 10. Disagree and Commit

Going back to the tree analogy: it's important to avoid too many parallel branches. Fragmented effort saps motivation and resources. People lose energy when they feel they're working on something ancillary to the primary objective.

It is the technology leader's responsibility to weigh options, hear the points and counterpoints, and make a decision about how to move forward. That may involve a quick feasibility experiment to inform the choice. But "let's try both" is, more often than not, a way to spend a lot of money, fragment attention, and not get anywhere.

Hear the disagreements, honor them, perhaps agree to revisit concerns later—but ultimately, everyone commits to the chosen direction and acknowledges the rationale.

## 11. Listen to Your Manufacturing Vendors

Engineers are about as close to manufacturing as most of us are to farming—which is to say, pretty far removed. When you look at injection molding, the mold itself is often more complicated than the part it produces.

When a manufacturing vendor tells you your tolerances are too tight, that your part will warp, or that you have yield risk on an adhesive process—listen. The earlier you bring manufacturing experience into the conversation, the fewer mistakes you'll make and the less money you'll spend.

## 12. Understand Software's Role

Even if you're a dedicated hardware developer, you need to understand the role software will play in your product. Virtually every product has a software component—whether it's embedded intelligence, cloud services, a user interface, or even just manufacturing quality control.

A friend recently told me, "Every company is a software company." She works for a major clothing retailer and she's a software developer. That statement resonates, especially now, when software can be worked into layers of business operations that were previously thought to require human decision-making. The least expensive solution to a problem is almost always a software solution.

## 13. Understand the Assignment

Are you building a proof of concept or a product? Are you collecting data and running an experiment, or designing something for an end user? Very often, early prototyping begins as proof-of-concept and ends with product design.

It's important to think about the user throughout, but don't get caught up in aesthetics and demos at the expense of confronting the core technical challenges—the ones most likely to fail. A good investor will look through a flashy demo and ask: How do you get the cost down? How do you avoid this blocking IP? How do you ensure adequate sensitivity? Be prepared to answer those questions, usually with a proof-of-concept breadboard prototype.

## 14. A Prototype Is Two Things: An Experiment and a Communication Tool

We often classify prototypes as "looks like," "feels like," "works like," or "is like"—each with a slightly different goal.

As a communication tool, putting something physical in the hands of an investor or user is incredibly powerful. People respond to physical prototypes far more strongly than to CAD models. Asking people to use a little imagination about what the device does while holding something tangible can unlock customer discovery interviews and inspire investors to open their minds—and their checkbooks.

But you want to pair these "looks like" and "feels like" prototypes with "works like" experimental validation: simple breadboards from off-the-shelf components that demonstrate the core science, combined with a well-articulated vision of how that science advances toward an integrated, cost-reduced product. At each prototype cycle, understand what this cycle is for and how to get the most from the investment.

## 15. Write Design Specs

In 2025, there is no excuse for not writing design specifications. AI makes writing design documents straightforward, and this is just good engineering practice. If you don't establish the goalpost, you won't know how you're scoring. This is particularly critical for client-facing work with payment milestones.

If your understanding isn't mature enough to write a spec, write an exploratory study plan that will lead to the data you need to shape the spec. That's the difference between feasibility and design. But not writing anything down—no expectations, no statement of work—is a recipe for disaster.

## 16. Learn to Work with Customers

Focus on their needs and educate them on potential solutions. Stay open to feedback. Don't get too attached to your own ideas. Understand that the goal is to solve problems. If you're not solving problems that impact other people, you're building art, not developing products.

## 17. Break Down the Problem

Systems thinking leads to subsystem definitions, which lead to components. At each interface, there's some input/output relationship to be defined—whether that's an API, a bus specification, or a mechanical interface. Within each subsystem, there's a set of behaviors, relationships, or state machines.

Break a system into block diagrams and understand the interfaces, behaviors, and relationships. This makes it possible to delegate effectively. It's often better to break things down in terms of engineering artifacts—this is a PCB, this is a manifold, this is a cartridge, this is a housing—rather than along traditional engineering disciplines, which can create silos. If you can specify a component with enough granularity—what it needs to do, where the I/O ports go, how much power it needs—you can hand it to a specialist and they can build it.

---

## A Core Curriculum for the Modern Engineer

The following is what we consider essential preparation for the kind of engineering we do—building hardware and software systems at the intersection of life sciences, medicine, and environmental sensing. It's opinionated, but broadly applicable.

### Physics

Get as much physics as you can, especially courses with hands-on demonstrations. Pay particular attention to electricity and magnetism, heat and mass transport, and fluid mechanics. Focus less on the calculus and more on developing intuition for the fundamental trade-offs: electromagnetic induction, motors, Lorentz force, the Hall effect, Fickian diffusion, convection, boundary conditions, scaling relationships, Reynolds numbers.

### Computing and Programming

Gain experience with embedded computers and microcontrollers. There are far more microcontrollers in the world than people, and once you understand what's possible through analog-to-digital conversion, sampling, embedded processing, and state machines, you can imagine countless applications. Prototyping has never been easier—Arduinos, STM32, ESP32, and Raspberry Pi are all readily available.

Learn Linux. It powers the internet, most software systems in the world, and embedded products. It's fully open source and free to use. Get comfortable at the command line.

Learn Python. If you're going to learn one programming language, make it Python—and learn to use it for data visualization, data processing, and text processing. If you're going to learn two, add C, so you understand how source code translates to machine code. Gain some understanding of computer architecture, networking (TCP/IP, REST APIs), and how computing systems communicate.

### Mechanical Engineering and Fabrication

Take a course in engineering mechanics if you'll be designing mechanical or electromechanical assemblies. A course in microfabrication is valuable if you'll work with microfluidics, MEMS, or integrated circuits. There are many product opportunities at the intersection of CMOS microfabrication, microfluidics, biology, and sensor technology.

### Chemistry and Biology

Organic chemistry is foundational for many sensing technologies that bridge the physical and digital worlds, and it underpins biochemistry and biology. Human physiology and anatomy are valuable not just professionally but personally. Cell biology—understanding metabolic pathways, cellular communication, division, and death—is essential for much of the work we do.

Note: we don't specifically recommend a course in microfluidics. The discipline is very applied, and university courses tend to focus narrowly on a professor's research interests. It's better to take the fundamentals and learn the state of the field through conferences and papers.

### Instrumentation and Signals

A course in basic instrumentation—signals and systems, linear time-invariant systems, control theory, PID controllers, sampling rate, Nyquist criterion, SNR, sources of noise—is fundamental to any engineering system involving sensing and control. These concepts directly impact clinical sensitivity and specificity in diagnostics and translate across signal modalities.

### Practical Skills

**CAD:** Learn a CAD tool. OnShape and SolidWorks are both excellent.

**Fabrication:** Learn 3D printing, CNC machining, laser cutting, PCB fabrication, and welding. Develop familiarity with supplier catalogs like McMaster-Carr and Digikey.

**Electronics troubleshooting:** Learn to use an oscilloscope, probe PCBs, and trace a signal path in a schematic starting from the power supply.

**Optics and imaging:** If you can, learn basic optics, imaging, and photonics. These are foundational in medical devices, life science tools, environmental sensing, and consumer electronics. Concepts like resolution, noise, and interference in imaging translate directly to other signal modalities.

---

*Mosaic Design Labs is an R&D studio in Berkeley, California, building biomedical instruments, diagnostic devices, and embedded systems. We believe the most talented engineers want to work on products that matter—not just products that make money.*