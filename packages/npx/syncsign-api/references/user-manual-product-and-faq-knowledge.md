# SyncSign Product, Integration, Firewall, and FAQ Knowledge Base

This document summarizes the official SyncSign user manual sections that are most useful when the user asks product questions, deployment questions, calendar-source questions, firewall questions, or common usage/FAQ questions.

Primary sources:
- User manual index: <https://dev.sync-sign.com/usermanual/>
- SyncSign Infrastructure Overview: <https://dev.sync-sign.com/usermanual/getstarted/infrastructure.html>
- On-Premise Server (SOPS) Setup: <https://dev.sync-sign.com/usermanual/install/on_premise_server.html>
- Firewall Configuration for Devices Linking with Cloud: <https://dev.sync-sign.com/usermanual/install/network_communication_cloud.html>
- Firewall Configuration for On-Premise Server (SOPS): <https://dev.sync-sign.com/usermanual/install/network_communication_on_premises.html>
- Network Requirements for Hub Device & Mobile Apps: <https://dev.sync-sign.com/usermanual/install/network_communication_on_hub_portal.html>
- Product Usage FAQ: <https://dev.sync-sign.com/usermanual/support/usage_faq.html>
- Calendar Data Source FAQ: <https://dev.sync-sign.com/usermanual/support/calendar_data_source_faq.html>
- Technical Specifications and Features: <https://dev.sync-sign.com/usermanual/support/technical_specifications_and_features.html>

## 1. When to Use This Reference

Use this file when the user asks about:
- what SyncSign products are and how the system is structured
- whether they should use SyncSign Cloud or SOPS
- which calendar data source to choose
- firewall requirements, allowed domains, or required ports
- common product usage questions already covered by the manual
- Microsoft 365 / calendar-source FAQ issues
- product capabilities, work modes, deployment advice, or model differences

Do not use this file as the main source for custom layout JSON authoring. For layout and template work, use `references/display-render-layout-knowledge.md`.

## 2. Product Architecture Overview

The official infrastructure overview describes four main parts:
- Calendar System for Booking
- SyncSign Server
- SyncSign Hub
- SyncSign Node

### Calendar System

This is the booking/calendar system the customer already uses for room reservations.

Officially documented examples:
- Google Calendar
- Google Workspace
- Office 365 / Microsoft 365
- Exchange Server

Important official note:
- Exchange Server requires an on-premise deployment. SyncSign SaaS Cloud does not connect directly to Exchange Server.

### SyncSign Server

The server side is used to:
- manage hubs and nodes
- handle OTA updates
- authorize calendar access
- associate displays with room calendars
- configure language, locale, logo, templates, and related settings

Two deployment modes are documented:
- `SaaS Cloud`
- `On-Premise`

### SaaS Cloud

Official positioning:
- online application
- forwards event-updated notifications to office hubs
- does not read or store event details in the cloud according to the infrastructure overview

### On-Premise

Official positioning:
- local deployment bridge between the booking system and SyncSign hubs/displays
- installed inside the customer's infrastructure
- suited for customers who want data to stay inside the corporate network

### SyncSign Hub

The hub acts as the bridge between nodes and the server.

Official responsibilities:
- manages multiple nodes such as displays and sensors
- stores calendar-system access keys
- fetches booking events from the calendar directly

### SyncSign Node

Nodes are the battery-powered endpoints such as displays and sensors.

Important display behavior:
- the hub sends rendering messages to the display
- the display renders text, images, or shapes
- the display does not store the rendering content

## 3. Cloud vs SOPS Guidance

### Choose SaaS Cloud when

- the customer wants the simplest setup
- no local server should be installed
- standard cloud calendar sources are sufficient

### Choose SOPS when

- the customer has special data-security or internal-network requirements
- Exchange Server integration is needed
- self-hosted or custom sources are needed, such as NextCloud, CalDAV, CSV URL, or Google Sheets

Official SOPS setup notes:
- SOPS supports multiple data sources
- documented examples include Google Calendar / G-Suite, Microsoft Office 365, Microsoft Exchange Server, NextCloud Calendar, CalDAV Calendar, CSV file, and Google Sheets
- the manual recommends setting up TLS for SOPS rather than using plain HTTP

## 4. Calendar Data Source Selection

The calendar-source FAQ gives these high-level choices:

| Data source | Typical use case | Deployment |
| --- | --- | --- |
| Google Calendar | Personal or small teams | SaaS or SOPS |
| Google Workspace / G Suite | Enterprise Google environment | SaaS or SOPS |
| Office 365 / Microsoft 365 | Microsoft 365 users | SaaS or SOPS |
| Exchange Server | On-premise Exchange | SOPS only |
| NextCloud | Self-hosted CalDAV server | SOPS only |
| CSV URL | Custom data source | SOPS only |

Practical selection guidance:
- `Google Calendar`: simplest personal/small-team path
- `Google Workspace`: enterprise Google path with resource management
- `Office 365`: Microsoft 365 path, supports organization/resource scenarios
- `Exchange Server`: requires SOPS
- `NextCloud`, `CalDAV`, `CSV URL`: require SOPS

Official deployment guidance:
- `SaaS`: suited for most users, simple configuration, no local server required
- `SOPS`: suited for enterprises with stricter data-security requirements

## 5. Cloud Integration Notes

For cloud integrations, the official manual has dedicated setup guides for:
- Google Calendar
- Google Workspace
- Office 365

For Office 365 / Microsoft 365, the FAQ explicitly says:
- standard commercial Microsoft 365 plans are supported
- examples listed include Business Basic, Business Standard, and Business Premium
- Microsoft GCC High is not supported
- personal Microsoft accounts are supported

### Common Microsoft 365 FAQ points

If room or shared calendars do not appear in SyncSign:
- verify the SyncSign-authorized account has appropriate calendar access
- for delegated mode, calendars under `My Calendars` are more reliably discoverable
- room/resource calendars under `Other Calendars` may be missed in delegated mode because of Graph API visibility behavior
- application-permission mode is more reliable for direct room mailbox access

Recommended investigation order from the FAQ:
1. Check permissions on the calendar or room resource.
2. If using delegated mode, make sure the calendar is under `My Calendars` or enumerate all calendar groups.
3. If using application permissions, confirm tenant admin consent.
4. Re-authorize and sign in again in the SyncSign client, then re-test synchronization.

If event titles show the organizer name instead of the subject:
- the FAQ says this is the default behavior of Office 365 room resources
- the fix is to change room resource settings so event titles are preserved

## 6. SOPS Integration Notes

SOPS supports multiple on-premise and custom source integrations.

Documented setup areas include:
- Microsoft 365
- Exchange Server
- Google Calendar / Google Workspace
- CalDAV on NextCloud
- CSV URL

Important SOPS usage notes:
- secure TLS is recommended
- the manual lists web portal, legacy portal, booking app, tablet app, and API endpoints under the SOPS domain
- SOPS can use webhooks for data sources that support change notifications
- for data sources without callback capability, polling can be used instead

## 7. Firewall and Network Guidance

### Devices Linking with SyncSign Cloud

If hubs connect to SyncSign Cloud, the manual says the firewall should allow outbound access to these core SyncSign services:
- TCP `8883` to `a1zjlbcv9qbzin-ats.iot.us-west-2.amazonaws.com` for MQTT remote notification
- TCP `443` to `api.sync-sign.com` for the SyncSign device/client API
- TCP `443` to `sync.sync-sign.com` for device health reporting
- TCP `443` to `update.sync-sign.com` for OTA updates
- TCP `443` to `file.sync-sign.com` for image assets / firmware resources
- TCP `80` to `pub.sync-sign.com` as a time-server fallback

Basic network services documented for cloud-connected hubs:
- UDP `123` to NTP services such as `pool.ntp.org` and `time.google.com`

Calendar-source outbound services documented for cloud-connected hubs:
- TCP `443` to `www.googleapis.com` for Google Calendar / Google Workspace
- TCP `443` to `graph.microsoft.com` for Office 365 / Microsoft 365

### Hub Portal and Mobile Apps

The manual also documents network requirements when using:
- Hub Portal
- mobile app
- cloud web portal

Important points:
- inbound TCP `80` to the hub's local IP is optional and mainly for Hub Portal access
- hub portal pages may require common CDN resources such as `unpkg.com`, `stackpath.bootstrapcdn.com`, `cdnjs.cloudflare.com`, `code.jquery.com`, and `cdn.jsdelivr.net`
- the mobile app / cloud web portal may require outbound TCP `443` to:
  - `portal.sync-sign.com`
  - `a1zjlbcv9qbzin-ats.iot.us-west-2.amazonaws.com`
  - `api.sync-sign.com`
  - `accounts.google.com`
  - `login.microsoftonline.com`
  - `dev.sync-sign.com`

### SOPS Firewall Guidance

The SOPS firewall document describes two common deployment patterns:
- all-in-LAN / VPN
- Internet + LAN

Important SOPS outbound requirements:
- OTA: `up.sync-sign.com`, `github.com`, `registry.hub.docker.com`, `docker.io`
- NTP: `pool.ntp.org`, `europe.pool.ntp.org`, `time.google.com`
- optional data sources:
  - `www.googleapis.com`
  - `graph.microsoft.com`

Important SOPS inbound requirements for hubs:
- TCP `8883`, `8443` for MQTT remote notification over secure protocols
- TCP `1883`, `8888` for MQTT remote notification over non-secure protocols
- TCP `80`, `443` for device/client API and admin portal

Important SOPS inbound requirement for data-source webhook:
- TCP `80`, `443` to the SOPS domain for data-updated webhooks

Important hub outbound access to SOPS / supporting services:
- SOPS domain on MQTT and API ports
- `sync.sync-sign.com`
- `update.sync-sign.com`
- `file.sync-sign.com`
- `pub.sync-sign.com`

## 8. Product Usage FAQ Summary

### Do all displays need a hub?

The official FAQ says:
- `2.9-inch` and `4.2-inch` displays must be used with a SyncSign Hub
- `7.5-inch` displays support both standalone mode and hub-connected mode

### When does a calendar-bound display refresh automatically?

The official FAQ lists these triggers:
- initial calendar binding
- event creation, deletion, or modification
- calendar status transitions such as:
  - no current activity -> activity scheduled
  - activity in progress -> activity ended

### How often does the display refresh?

Official FAQ summary:
- with a Hub: when a new rendering task is generated, the Hub sends parsed rendering data to the display
- in standalone mode: the refresh interval can be configured in the display web portal

### Display refresh failure: quick split

The usage FAQ suggests this troubleshooting split:
- if a `Draw on Screen` test also fails, suspect the SyncSign Cloud Server -> Hub -> Display chain
- if `Draw on Screen` succeeds but the calendar does not refresh, check the current calendar data source and follow the calendar FAQ

### Defects in calendar template layout

FAQ guidance:
- if certain field contents do not display, the preset template area may be too small
- if the logo is incomplete, verify the logo image specifications

Logo requirements documented in the FAQ:
- monochrome BMP
- `1-bit` depth
- square image up to `96 x 96`
- size under `100KB`

### Can users create their own calendar templates?

Yes.

Official client path:
- `Settings -> Organization -> Customized Templates`

Official documentation path:
- render layout guide for general template field definitions
- calendar template editing guide for calendar-specific placeholders

## 9. Technical Specifications and Feature Notes

### Display model families

The technical-specifications page distinguishes:
- BLE-based displays
- ZigBee-based displays

Documented examples include `2.9-inch`, `4.2-inch`, and `7.5-inch` variants.

### Color support

The technical-specifications page lists models with:
- black/white/red
- black/white
- black/white/red/yellow

Do not generalize color capability across all models. If the exact model matters, answer carefully and say when the manual shows different capabilities for BLE vs ZigBee variants.

### Hub indicator meanings

Official meanings:
- `Purple breathing`: normal working state, connected to Internet
- `Blue flashing`: setup mode / pairing mode
- `Red flashing`: network connection failure / offline
- `Off`: powered off or hardware failure

### Deployment advice

Official deployment advice includes:
- keep Hub and Display close to each other
- place them higher in the same space when possible
- avoid obstacles and interference sources
- for BLE deployments, the manual gives approximate line-of-sight distances and recommends planning for stability rather than theoretical maximum range
- when deploying multiple hubs in the field, placing BLE displays within scanning range of multiple hubs can improve stability

### 7.5-inch BLE side button notes

The technical-specifications page says:
- the sliding side button currently has no functional purpose and is reserved
- the pinhole button is for setup mode
- the external button can be used for manual refresh, Wi-Fi setup/IP display, or reset in the documented standalone workflow

If the user's environment follows stronger maintainer guidance for this repository, that maintainer guidance should take precedence over older generic manual behavior claims.

## 10. How the Agent Should Answer from This Reference

When answering user questions from this document:
- prefer direct answers when the FAQ clearly covers the issue
- clearly separate `Cloud` guidance from `SOPS` guidance
- do not recommend Exchange Server with SaaS Cloud
- do not overclaim exact model capabilities when the manual varies by BLE vs ZigBee model family
- if the user's issue is already covered by the calendar FAQ, answer with the documented investigation order before inventing a custom diagnosis
- if the user's issue is mainly network-related, answer with the relevant domain/port checklist
- if the issue is not covered well enough by the manual, say so and direct the user to:
  - <https://help.sync-sign.com>
  - `help@sync-sign.com`
