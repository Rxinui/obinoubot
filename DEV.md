Feature: one single bot for multiple chats.

Issues:
- How to route message to right chats.
- How to route message content according to user.

Scenarios:
- Group A and B
- Users: A1,A2 and B1
- When B1 use '/newpr' and submit => Bot will notify B1's group about it's PR.
  - How to identify B1's group ?
  - How to ensure that bot notify the right group ?
  - How to fetch right group information ?

Steps:
1. B1 use `newpr` command then submit
2. Bot fetch B1's data:
  - its username
  - its group
3. Bot fetch groups' resources/property:
  - lookup for resource in order to instantiate service
4. Bot instantiate service and use it

-------
Feature: use bot to interact with Google Sheet

Issues: 
- How to fetch the right bloc program
- How to verify that bloc is compatible with this functions
- States diagram of the bot

Command:
- /startworkout - begin the assistance to workout

States: a state represent the moment where Bot is waiting for specifics instructions triggered by a command from user
- A. SPREADSHEET_INPUT (ONETIME)
- B. WEEK_NUMBER_INPUT (ONETIME)
- C. DAY_INPUT (ONETIME)
- D. AWAIT_NEXT_SET (MULTIPLE)
- E. AWAIT_END_OF_REST_TIME (MULTIPLE)
- F. AWAIT_LOG_SUCCESS (MULTIPLE)
- G1. AWAIT_LOG_RIR (MULTIPLE)
- G2. AWAIT_LOG_KG (MULTIPLE)
- H. AWAIT_LOG_MESSAGE (MULTIPLE)

Internal states: a state where Bot is not waiting for a user prompt but for a state to be triggered before executing a function

- Int1: LOAD_EXERCISE
- Int2: EXERCISE_COMPLETED

Conversation commands:
- c0: $spreadsheetURL
- c1: $week_number (int)
- c2: $day_value (int | str)
- c3: nextSet
- c4: skipExercice
- c5: $logOK (SUCCESS | FAILED)
- c6: $logRIR (RIR0 | RIR1 | RIR2 | RIR3 | RIR4 | RIR5)
- c7: $logKG
- c8: $logMessage
- cA: cancel

Actions: process that is executed by internal states
- a1: send message to user which indicate exercise to do and its information
- a2: launch a timer and wait until it ends before sending notification message

Transitions: (--> means *triggers* and --? means *awaits*)
A --> c0
c0 --> B --? c1
c1 --> C --? c2
c2 --> Int1 --> a1
a1 --> D --? c3 | c4 | cA
c3 --> D --? c3 | c4 | cA
c3 --> E  --> a2
c3 --> Int1
a2 --> Int1
a2 --> D
a2 --> Int2 --> Int1
Int2 --> F --? c5
c4 --> D --? c3 | c4 | cA
c5 --> G1 --? c6
c5 --> G2 --? c7
c6,c7 --> H --? c8
c8 --> D --? c3 | c4 | cA
c8 -->END
cA --> END
