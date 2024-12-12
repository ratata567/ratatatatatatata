<script lang="ts">
	import { getAdminDetails } from '$lib/apis/auths';
	import { onMount, tick, getContext } from 'svelte';
	import { WEBUI_NAME } from '$lib/stores';

	const i18n = getContext('i18n');

	let adminDetails = null;

	onMount(async () => {
		adminDetails = await getAdminDetails(localStorage.token).catch((err) => {
			console.error(err);
			return null;
		});
	});
</script>

<div class="fixed w-full h-full flex z-[999]">
	<div
		class="absolute w-full h-full backdrop-blur-lg bg-white/10 dark:bg-gray-900/50 flex justify-center"
	>
		<div class="m-auto pb-10 flex flex-col justify-center">
			<div class="max-w-md">
				<div class="text-center dark:text-white text-2xl font-medium z-50">
					{$i18n.t('Account Activation Pending')}
				</div>

				{#if $WEBUI_NAME === "Anvil GPT"}
					<div class=" mt-4 justify-start text-sm dark:text-gray-200 w-full">
						{$i18n.t('Your account status is currently pending. For approval, please reach out to the ACCESS help desk')} <a href="https://support.access-ci.org/open-a-ticket">(https://support.access-ci.org/open-a-ticket)</a> {$i18n.t('with the subject/summary line “AnvilGPT Access Request”. Select "Some Other Question" as the user support issue and "Anvil" as the resource.')}
						<br /><br />
						{$i18n.t('In the description of your ticket, provide a brief description of how you intend to use the service, your allocation number, and if you intend to use the UI, API, or both.')}
						<br /><br />
						{$i18n.t('An admin will assess and approve your request and get back to you.')}
					</div>
				{:else if $WEBUI_NAME === "Purdue GenAI Studio"}
					<div class=" mt-4 justify-start text-sm dark:text-gray-200 w-full">
						{$i18n.t('Your account is currently pending. If an admin does not approve your request within the next 2 business days, please reach out the RCAC help desk')} <a href="mailto:rcac-help@purdue.edu">(rcac-help@purdue.edu)</a> {$i18n.t('with the subject/summary line "GenAI Studio Access Request.”')}
						<br /><br />
						{$i18n.t('In the description of your ticket, provide a brief description of how you intend to use the service, and if you intend to use the UI, API, or both.')}
						<br /><br />
						{$i18n.t('An admin will assess and approve your request and get back to you.')}
					</div>
				{:else}
					<div class=" mt-4 justify-start text-sm dark:text-gray-200 w-full">
						{$i18n.t('Your account status is currently pending.')}
						<br /><br />
						{$i18n.t('An admin will assess and approve your request and get back to you.')}
					</div>
				{/if}

				<div class=" mt-6 mx-auto relative group w-fit">
					<button
						class="relative z-20 flex px-5 py-2 rounded-full bg-white border border-gray-100 dark:border-none hover:bg-gray-100 text-gray-700 transition font-medium text-sm"
						on:click={async () => {
							location.href = '/';
						}}
					>
						{$i18n.t('Check Again')}
					</button>

					<button
						class="text-xs text-center w-full mt-2 text-gray-400 underline"
						on:click={async () => {
							localStorage.removeItem('token');
							location.href = '/auth';
						}}>{$i18n.t('Sign Out')}</button
					>
				</div>
			</div>
		</div>
	</div>
</div>
