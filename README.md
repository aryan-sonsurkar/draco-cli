## draco-cli

Draco is a command-line assistant built step by step while learning Python.  
The project emphasizes clean architecture, modular design, and practical automation rather than isolated scripts.

Draco is designed as a real, extensible CLI system capable of combining automation, AI assistance, and workflow optimization.

---

## Purpose

- Practice Python fundamentals  
- Build real-world automation skills  
- Improve debugging and problem-solving ability  
- Develop a system-level CLI assistant  

---

## Core Features

- Interactive command-line interface  
- Text and Voice Mode  
- Text-to-Speech (pyttsx3)  
- Modular architecture (commands, brain, automations, AI modules)  
- Easy command extensibility  

---

## Automation & System Capabilities

- Website launcher  
- File and folder opener  
- Human-like typing automation  
- Smart web search with AI analysis  
- End-of-Day Wind Up System  
- Quick Actions Hub  
- Arrival Routine (Jarvis Mode)  
- Pomodoro / Study Timer  
- Practical Manager  
- Scheduled Guild Wars Alert  
- Command Center (OS-style live interface)

### WhatsApp File Transfer Automation

Draco now supports OS-level file sharing automation through WhatsApp Desktop.

Users can copy any file directly from the operating system and instruct Draco to send it without manually navigating file dialogs.

Draco detects files from the clipboard, launches WhatsApp Desktop, performs visual interface recognition, and executes deterministic UI interactions to complete the file upload process.

Automation flow:

• Detect WhatsApp interface  
• Click Attach Button  
• Select Document Upload  
• Inject File Path  
• Trigger Send Action  

Key capabilities:

- Clipboard-based file detection  
- Visual UI automation using image recognition  
- Automatic WhatsApp launch  
- Document upload workflow automation  
- Hands-free file transfer interaction  

Example usage:

1. Select any file in File Explorer  
2. Press Ctrl+C  
3. Run Draco command:

send file on whatsapp

Draco will complete the remaining interaction automatically.

---

## AI Capabilities (Ollama)

- AI-powered calculator  
- AI fallback engine  
- Algorithm generator  
- Essay writer  
- Explainer mode  
- Code Explainer  
- Question Generator from Notes  
- Project Generator Engine  

---

## Academic Utilities & Learning Utilities

- Syllabus Intelligence System  
  - Current subjects: C Programming, Data Structures  

- Question Generator from Notes  
  - Generates Viva, MCQs, Short & Long Questions  

- C Boilerplate Writer  

- Assignment Writer & Enhancer 

- Adaptive AI Tutor System  

  Draco operates as a personalized learning assistant:

  • Train by Topic (Skill Tutor)  
  • Train from Saved Notes (Notes Tutor)  
  • Weak Concept Tracking  
  • AI-Powered Conceptual Grading  
  • Reinforcement-Based Questioning

---

- Adaptive AI Teaching System (Skill Tutor + Notes Tutor)

Draco now functions as an intelligent teaching machine powered by Ollama.

- Skill Tutor Mode  
  Draco generates dynamic conceptual questions from any topic provided by the user.

- Notes Tutor Mode  
  Users can store their own study notes and let Draco generate infinite questions directly from saved material.

- AI-Based Evaluation  
  Answers are evaluated conceptually using Ollama instead of fragile string matching.

- Weakness Memory Engine  
  Incorrectly answered questions are stored automatically and revisited later for reinforcement learning.

- Adaptive Revision Behavior  
  Questions previously answered incorrectly are prioritized until mastered.

- Persistent Notes Storage  
  Notes can be saved once and reused anytime for AI-driven practice sessions.

---

## Project Generation Engine

Draco can generate project code from natural language descriptions and type them directly into an editor.

Example commands:

draco project  
project creator

---

## Tutor Commands

train skill        → Practice any topic using AI-generated questions  
save notes         → Store study material for future sessions  
train notes        → Generate questions from saved notes  
show weak          → View previously missed questions  
clear weak         → Reset weakness memory  

---

## Example Commands

- who are you  
- system status  
- open website github  
- note add / note show  
- generate questions  
- syllabus show c programming  
- command center  
- practical list / practical done  
- draco project  
- send file on whatsapp  
- end of the day  
- help  

---

## How to Run

1. Install Ollama and required model (e.g., llama3)  
2. Clone the repository  
3. Install dependencies from requirements file  
4. Run the main Python file  

---

## Status

Work in progress.  
Draco is continuously evolving with new automation systems, AI features, and usability improvements.

---

## Author

Aryan Sonsurkar  
Computer Engineering Student  
Focused on Python, automation, CLI systems, and AI-driven workflows
