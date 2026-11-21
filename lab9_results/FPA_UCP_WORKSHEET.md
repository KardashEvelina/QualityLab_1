# TASK 3 — FPA & UCP WORKSHEET

## Selected business submodule

Apache ActiveMQ Web Console — message and destination management.

Selected classes:
- SendMessage
- DestinationFacade
- WebClient
- BrokerFacade
- CreateDestination

## Source Evidence

Observed operations:
- SendMessage.handleRequest(...)
- SendMessage.sendMessages(...)
- SendMessage.createMessage(...)
- DestinationFacade.addDestination(...)
- DestinationFacade.removeDestination(...)
- CreateDestination.handleRequest(...)
- WebClient.send(...)
- WebClient.getProducer(...)
- WebClient.getConsumer(...)

HTTP evidence:
- SendMessage: POST
- CreateDestination: POST

---

# FPA

## Data Functions

JMS Message data = EIF | Complexity: Low | Weight: 5
Destination data = EIF | Complexity: Low | Weight: 5
Broker/JMS resources = EIF | Complexity: Low | Weight: 5

## Transactional Functions

Send message = EI | Complexity: Low | Weight: 3
Create destination = EI | Complexity: Low | Weight: 3
Remove destination = EI | Complexity: Low | Weight: 3
Browse destination = EQ | Complexity: Low | Weight: 3


## FPA Result

TOTAL FP = 27

# UCP

## Actors

Web Console user = Complex | Weight: 3
Broker/JMS subsystem = Medium | Weight: 2

## Use Cases

Send Message = 4 transactions | Medium | Weight: 10
Create Destination = 3 transactions | Simple | Weight: 5
Remove Destination = 3 transactions | Simple | Weight: 5
Browse Destination = 5 transactions | Medium | Weight: 10

## Calculations

UAW = 5
UUCW = 30
UUCP = 35
TCF = 1.0
ECF = 1.0
UCP = 35
Real person-hours = ___
PF = ___
