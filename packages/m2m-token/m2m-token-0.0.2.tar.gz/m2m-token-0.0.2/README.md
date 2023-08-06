# M2M Token

Here is the issue : You have a Bot and a REST Api that needs to communicate. 
As the REST Api is an entrypoint to your system, you don't want it to be unsecured (at least you should not want that.)
At the same time, you don't want them to have plain text password configured somewhere, because, it can be guessed.

And you don't want to implement a full-fledged 2-ways SSL authentication, because, well, it is complicated.

## So what to do then ?
It'd be nice if we had a way to have a token that changes regularly but can still be guessed by involved parties.

This is something that has been (still ?) done on automated garage doors. Ever wondered how come your remote does not
open the garage door of your neighbor ? It's because it uses a [Rolling Code](https://en.wikipedia.org/wiki/Rolling_code)
which is a quite simple technique but still pretty efficient.

## How does it works ?
The same as in the rolling code for the RF remote controller, both parties (Bot and REST Api for instance),
are going to share a `seed`. This seed will be used to generate a token on both sides, this way we can check that
the Bot is indeed authorize to use the REST Api.

The parties are also going to agree on the token `ttl` (Time To Live), this should prevent attacker
from sending an outdated token to the REST Api and be granted access.

## How to use ?

### Installation
`pip install m2m_token`

### Token Generation
```python
from m2m_token.token import generate

seed = 'VeryComplicatedSeedSoThatItIsReallyHardForTheAttackerToGuessIt'
ttl = 3  # Time in seconds the token is going to be valid.

# On the bot side:
bot_token = generate(seed, ttl)
# Add the generated token to the REST Http request

# On the API side:
def method_that_handles_request(request):
    token = find_token_in_request(request)
    if token !=  generate(seed, ttl):
        raise NotAllowed()
```

### `generate()` Parameters
Parameter|Description|Mandatory|Default Value
---|---|---|---|
`seed`|The seed to generate the token|Yes|N/A
`ttl`|Time in seconds the token is valid|Yes|N/A
`sequence`|Characters sequence from wich the token will be generated|No|`string.ascii_letters + string.digits`
`token_len`|Generated token length|No|6

## Disclaimer
This comes without any warranties of any sorts. 
I can not be hold responsible if you ever stumble upon this and decide to do something evil with it (like training some raccoon to hold a bazooka and go berserk with it).

More seriously, this has not been tested by real pentesters (if any are willing I'd be more than glad to have feedbacks)

Pull requests, issues may or may not be handled but are always welcomed.
