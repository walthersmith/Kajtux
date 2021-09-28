import operator
from typing import List, Optional

from discord import Message, Embed, Color

def filterReactionCount(message: Message, acceptedReactions: Optional[List[str]] = []):
    reactionsCount = dict(
        (str(reaction.emoji), reaction.count - 1)
        for reaction in message.reactions
        if(str(reaction.emoji) in acceptedReactions or acceptedReactions == [])
    )
    maxVoted = max(reactionsCount.values())
    mostVoted = None if maxVoted == 0 else list(filter(lambda react: reactionsCount[react] == maxVoted, reactionsCount))

    reactionsCount['totalVotes'] = maxVoted
    reactionsCount['mostVoted'] = mostVoted if reactionsCount['totalVotes'] > 0 else None

    return reactionsCount

def getVoteDetails(message: Message):
    embed = message.embeds[0]
    voteDetails = {
        'question': embed.title,
        'answers': embed.description.split('\n') if embed.description else None,
        'stats': embed.footer.text,
        'author': embed.author,
        'timestamp': embed.timestamp,
        'reactions': filterReactionCount(message)
    }

    return voteDetails

def voteDetailsToEmbedVote(voteDetails: dict):
    embed = Embed(
        title=voteDetails['question'],
        description='\n'.join(voteDetails['answers']),
        colour=Color.purple()
    )
    embed.set_author(name=voteDetails['author'].name, icon_url=voteDetails['author'].icon_url)
    embed.set_footer(text=voteDetails['stats'])
    embed.timestamp = voteDetails['timestamp']

    return embed
