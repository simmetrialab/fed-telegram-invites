#!/usr/bin/env python

import os
import time
import asyncio
import logging
from telethon import TelegramClient
from pyairtable import Table
from pyairtable.formulas import match
from apscheduler.schedulers.blocking import BlockingScheduler

api_id = os.environ['TELEGRAM_API_ID'];
api_hash = os.environ['TELEGRAM_API_HASH'];
airtable_api_key = os.environ['AIRTABLE_API_KEY'];
airtable_table_id = os.environ['AIRTABLE_TABLE_ID'];

loop = asyncio.get_event_loop()

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

async def get_telegram_members():
    logging.info("Retrieve channel members...")
    users = await client.get_participants('@frontend_daily')
    return users

def get_pending_invites():
    logging.info('Retrive pending invites...')
    formula = match({ "inviteStatus": "Pending" })
    records = table.all(fields=['invitedID'], formula=formula)
    return list(records)

def find_targets(pending_invites, members_ids):
    logging.info('Finding joined invites...')
    targets = []
    for invite in pending_invites:
        invited_id = invite.get('fields', {}).get('invitedID')
        if invited_id in members_ids:
            targets.append(invite)
    return targets

def update_targets_status(targets):
    logging.info('Updating invites status...')
    for target in targets:
        table.update(target['id'], { "inviteStatus": "Joined" })

def main():
    members = loop.run_until_complete(get_telegram_members())
    members_ids = list(map(lambda x: str(x.id), members))
    pending_invites = get_pending_invites()
    targets = find_targets(pending_invites=pending_invites, members_ids=members_ids)
    if (len(targets) == 0):
        logging.info('No joined invites founded!')
    else:
        update_targets_status(targets=targets)
    logging.info('Job done!')

if __name__ == "__main__":
    try:
        with open('FEDChallange.session') as f:
            logging.info('Telegram session file present.')
    except IOError:
        logging.error("Missing Telegram session file")
        exit()

    client = TelegramClient('FEDChallange', api_id, api_hash)
    table = Table(airtable_api_key, airtable_table_id, 'Invites')

    with client:
        scheduler = BlockingScheduler()
        scheduler.add_job(main, 'interval', seconds=5)
        scheduler.start()
        logging.info("Scheduler started")