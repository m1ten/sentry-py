import discord


async def perms(interaction: discord.Interaction, perms: str or list(str) = None, user: discord.User = None) -> str:

    # get hierarchy
    author_hi = interaction.guild.get_member(
        interaction.user.id).top_role.position

    # get user hierarchy
    user_hi = interaction.guild.get_member(
        user.id).top_role.position if isinstance(user, discord.member.Member) else -1

    # get bot hierarchy
    bot_hi = interaction.guild.get_member(
        interaction.client.user.id).top_role.position

    # check hierarchy
    if author_hi and bot_hi > user_hi:
        if perms:
            permissions = []
            for perm in perms.split() if isinstance(perms, str) else perms:
                try:
                    if (perm == 'bot_owner') == await interaction.client.is_owner(interaction.user):
                        permissions.append(perm)
                    elif interaction.permissions.__getattribute__(perm.lower()):
                        permissions.append(perm)
                    else:
                        return f'{perm} = Insefficient'
                except AttributeError:
                    return f'{perm} = Invalid'

            return f'{permissions} = Success'
        else:
            return 'NotSpecified'
    else:
        return 'Denied'
