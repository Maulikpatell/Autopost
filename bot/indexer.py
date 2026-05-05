async def update_source(client, source_id, admins, messages_col):
    doc = await messages_col.find_one({"source_id": source_id})
    existing_ids = doc["message_ids"] if doc else []

    last_id = max(existing_ids) if existing_ids else 0

    msgs = await client.get_messages(source_id, min_id=last_id)

    new_ids = [m.id for m in msgs if m.id not in existing_ids]

    if new_ids:
        updated = existing_ids + sorted(new_ids)

        await messages_col.update_one(
            {"source_id": source_id},
            {"$set": {"message_ids": updated}},
            upsert=True
        )

        for admin in admins:
            await client.send_message(
                admin,
                f"✅ Indexed {len(new_ids)} new posts from {source_id}"
            )
