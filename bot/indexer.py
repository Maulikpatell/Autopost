async def update_source(client, source_id, admins, messages_col):
    msgs = await client.get_messages(source_id, limit=100)

    doc = await messages_col.find_one({"source_id": source_id})
    existing = set(doc["message_ids"]) if doc else set()

    new_ids = [m.id for m in msgs if m.id not in existing]

    if new_ids:
        updated = list(existing) + sorted(new_ids)

        await messages_col.update_one(
            {"source_id": source_id},
            {"$set": {"message_ids": updated}},
            upsert=True
        )

        for admin in admins:
            await client.send_message(
                admin,
                f"✅ Source Updated\n\nSource: {source_id}\nNew: {len(new_ids)}\nTotal: {len(updated)}"
            )
