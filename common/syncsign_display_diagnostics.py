from __future__ import annotations

from datetime import datetime, timezone


SUPPORTED_CALENDAR_MODELS = {"D75C-LEWI", "D42C-LE", "D29C-LE"}
TWENTY_FOUR_HOURS_MS = 24 * 60 * 60 * 1000
SUPPORT_URL = "https://help.sync-sign.com"
SUPPORT_EMAIL = "help@sync-sign.com"


def utc_iso_from_unix_ms(value):
    if value is None:
        return None
    return datetime.fromtimestamp(value / 1000, tz=timezone.utc).isoformat()


def parse_int(value):
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def extract_online_status(data):
    if not isinstance(data, dict):
        return None

    candidates = [
        data.get("onlined"),
        data.get("online"),
        data.get("isOnline"),
        data.get("connected"),
        ((data.get("info") or {}).get("network") or {}).get("connected"),
        ((data.get("network") or {}).get("connected")),
    ]
    for value in candidates:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"online", "on", "connected", "true"}:
                return True
            if normalized in {"offline", "off", "disconnected", "false"}:
                return False

    status = data.get("status")
    if isinstance(status, str):
        normalized = status.strip().lower()
        if normalized in {"online", "connected"}:
            return True
        if normalized in {"offline", "disconnected"}:
            return False

    return None


def support_actions():
    return [
        f"There is not enough information from the API to continue this diagnosis. Please contact SyncSign Support at {SUPPORT_URL} or {SUPPORT_EMAIL}."
    ]


def evaluate_calendar_binding(node):
    calendar = node.get("calendar")
    if not isinstance(calendar, dict):
        return {
            "calendar_bound": False,
            "calendar_data": None,
            "watch_resource_id": None,
            "watch_expiration_ms": None,
            "watch_expiration_utc": None,
            "watch_expires_within_24h": False,
            "calendar_subscription_success": False,
            "calendar_subscription_reason": "No calendar field was returned for this display.",
        }

    has_calendar_info = any(value not in (None, "", [], {}) for value in calendar.values())
    watch_resource_id = calendar.get("watchResourceId")
    watch_expiration_ms = parse_int(calendar.get("watchExpiration"))
    watch_expiration_utc = utc_iso_from_unix_ms(watch_expiration_ms)

    return {
        "calendar_bound": has_calendar_info,
        "calendar_data": calendar,
        "watch_resource_id": watch_resource_id,
        "watch_expiration_ms": watch_expiration_ms,
        "watch_expiration_utc": watch_expiration_utc,
    }


def evaluate_calendar_subscription(node, now_ms):
    result = evaluate_calendar_binding(node)
    if not result["calendar_bound"]:
        return result

    watch_resource_id = result["watch_resource_id"]
    watch_expiration_ms = result["watch_expiration_ms"]

    if not watch_resource_id or watch_expiration_ms is None:
        result["watch_expires_within_24h"] = False
        result["calendar_subscription_success"] = False
        result["calendar_subscription_reason"] = (
            "The display has a bound calendar, but watchResourceId or watchExpiration is missing."
        )
        return result

    if watch_expiration_ms <= now_ms:
        result["watch_expires_within_24h"] = False
        result["calendar_subscription_success"] = False
        result["calendar_subscription_reason"] = "The calendar subscription has expired."
        return result

    delta_ms = watch_expiration_ms - now_ms
    within_24h = delta_ms <= TWENTY_FOUR_HOURS_MS
    result["watch_expires_within_24h"] = within_24h
    result["calendar_subscription_success"] = within_24h
    if within_24h:
        result["calendar_subscription_reason"] = (
            "watchResourceId is present and watchExpiration is still within the next 24 hours."
        )
    else:
        result["calendar_subscription_reason"] = (
            "watchExpiration is present but is not within the expected next 24 hours."
        )
    return result


def build_offline_actions(model, battery_level, signal_level, hub_online):
    actions = []
    notes = [
        "Display battery and signal readings are the most recent values reported while the display was still online."
    ]

    if hub_online is False:
        actions.append(
            "Check whether the nearby Hub is offline. Restore the Hub first by power cycling it or re-adding it in the app."
        )
        return actions, notes

    if hub_online is True:
        notes.append("The Hub appears to be online, so the display issue is more likely local to the display.")
    else:
        notes.append("Hub online status could not be confirmed from the available API response.")
        actions.extend(support_actions())
        return actions, notes

    if battery_level is not None and battery_level < 15:
        if model in {"D75C-LEWI", "D42C-LE"}:
            actions.append(
                "Battery is below 15%. Charge the display with the matching power adapter and power cable."
            )
        elif model == "D29C-LE":
            actions.append("Battery is below 15%. Replace the AA 1.5V batteries.")

    if signal_level is not None and signal_level < 30:
        actions.append(
            "Signal is below 30%. Reposition the Hub and display higher in the space and away from obstacles or interference sources."
        )
        actions.append(
            "While adjusting placement, press the display pinhole button for 1 second and confirm that Last Seen updates to the current time in the SyncSignr app. If it does, the displayed signal level is the real current signal."
        )
        notes.append("A signal level above 30% is recommended for stable operation.")

    if not actions:
        actions.extend(support_actions())
        notes.append(
            "The available API fields do not identify a clear battery, signal, or Hub cause for this offline display."
        )

    return actions, notes


def diagnose_display_sync(node, now_ms, hub_detail=None):
    model = node.get("model")
    display_online = extract_online_status(node)
    hub_sn = node.get("thingName")
    hub_online = extract_online_status(hub_detail)
    battery_level = parse_int(node.get("batteryLevel"))
    signal_level = parse_int(node.get("signalLevel"))
    last_seen_ms = parse_int(node.get("lastSeen"))

    diagnosis = {
        "supported_model": model in SUPPORTED_CALENDAR_MODELS,
        "model": model,
        "supported_models": sorted(SUPPORTED_CALENDAR_MODELS),
        "display_online": display_online,
        "hub_sn": hub_sn,
        "hub_online": hub_online,
        "battery_level": battery_level,
        "signal_level": signal_level,
        "last_seen_ms": last_seen_ms,
        "last_seen_utc": utc_iso_from_unix_ms(last_seen_ms),
        "support_url": SUPPORT_URL,
        "support_email": SUPPORT_EMAIL,
        "actions": [],
        "notes": [],
    }

    if model not in SUPPORTED_CALENDAR_MODELS:
        diagnosis["summary"] = (
            "This diagnostic flow is only available for models D75C-LEWI, D42C-LE, and D29C-LE."
        )
        diagnosis["actions"].extend(support_actions())
        return diagnosis

    calendar_result = evaluate_calendar_subscription(node, now_ms)
    diagnosis.update(calendar_result)

    if display_online is False:
        diagnosis["summary"] = "The display is offline."
        actions, notes = build_offline_actions(model, battery_level, signal_level, hub_online)
        diagnosis["actions"].extend(actions)
        diagnosis["notes"].extend(notes)
        return diagnosis

    if display_online is None:
        diagnosis["summary"] = "There is not enough information from the API to determine whether the display is online."
        diagnosis["actions"].extend(support_actions())
        return diagnosis

    if not diagnosis["calendar_bound"]:
        diagnosis["summary"] = "The display is online, but no calendar is currently bound."
        diagnosis["actions"].append(
            "Bind a calendar from the display configuration page in the SyncSign client."
        )
        return diagnosis

    if not diagnosis["calendar_subscription_success"]:
        diagnosis["summary"] = "The display is online, but the calendar subscription is not healthy."
        diagnosis["actions"].append(
            "Unbind the calendar from the display and bind it again, then check whether the display can sync and refresh."
        )
        return diagnosis

    diagnosis["summary"] = "The display is online, the calendar is bound, and the calendar subscription appears healthy."
    diagnosis["notes"].append(
        "This result is based only on the API fields that were returned. If sync refresh still fails, this workflow did not find a calendar binding or subscription issue."
    )
    return diagnosis

