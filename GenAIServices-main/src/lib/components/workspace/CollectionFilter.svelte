<script>

	import { DropdownMenu } from 'bits-ui';
    import {documents, created_collections, collection_filtered_documents, mobile } from '$lib/stores';
	import { flyAndScale } from '$lib/utils/transitions';
	import ChevronDown from '$lib/components/icons/ChevronDown.svelte';
	import { deleteCollectionByName, getCollections } from '$lib/apis/collections';
	import { toast } from 'svelte-sonner';




    export let selected_collection = 'All Documents';
	export let className = 'w-[30rem]';
	let collectionCount = {};

    // export let collection_filtered_documents = $documents;

    $ : {
        $collection_filtered_documents = $documents
        handleCollectionChange()
    }
	$ :{
			collectionCount = $documents.reduce((acc, item) => {
      acc[item.collection_name] = (acc[item.collection_name] || 0) + 1;
      return acc;
    }, {});
	console.log(collectionCount)
	}


	let show = false;
	let searchValue = '';
	let placeholder = 'All Documents'	


    function handleCollectionChange(){
        if(selected_collection == 'All Documents'){
            $collection_filtered_documents = $documents
        }
        else{
            $collection_filtered_documents = $documents.filter((document)=> document.collection_name == selected_collection)
        }
        

    }
	async function handleCollectionDelete(collection_name){
		if(collectionCount[collection_name]){
			toast.error('Collection is not empty');
		}
		else{
		deleteCollectionByName(localStorage.token, collection_name);
		await created_collections.set(await getCollections(localStorage.token));
		}
	}
</script>

<!-- <h1>Select Collection</h2> -->

<!-- <form on:submit|preventDefault={handleSubmit}> -->
	<!-- <select bind:value={selected_collection} on:change={() => (handleCollectionChange())}>
        <option value='All Documents'>
            'All Documents'
        </option>
		{#each $created_collections as collection}
			<option value={collection.collection_name}>
				{collection.collection_name}
			</option>
		{/each}
	</select> -->

	<!-- <input bind:value={answer} />

	<button disabled={!answer} type="submit"> Submit </button> -->
<!-- </form> -->

<!-- <p>selected question {selected ? selected.id : '[waiting...]'}</p> -->

<DropdownMenu.Root
	bind:open={show}
	onOpenChange={async () => {
		searchValue = '';
		window.setTimeout(() => document.getElementById('model-search-input')?.focus(), 0);
	}}
>
	<DropdownMenu.Trigger class="relative w-full" aria-label={placeholder}>
		<div
			class="flex w-full text-left px-0.5 outline-none bg-transparent truncate text-lg font-semibold placeholder-gray-400 focus:outline-none"
		>
			{selected_collection}
			<ChevronDown className=" self-center ml-2 size-3" strokeWidth="2.5" />
		</div>
	</DropdownMenu.Trigger>

	<DropdownMenu.Content
		class=" z-40 {$mobile
			? `w-full`
			: `${className}`} max-w-[calc(100vw-1rem)] justify-start rounded-xl  bg-white dark:bg-gray-850 dark:text-white shadow-lg border border-gray-300/30 dark:border-gray-700/50  outline-none "
		transition={flyAndScale}
		side={$mobile ? 'bottom' : 'bottom-start'}
		sideOffset={4}
	>
		<slot>
			<!-- {#if true}
				<div class="flex items-center gap-2.5 px-5 mt-3.5 mb-3">
					<Search className="size-4" strokeWidth="2.5" />

					<input
						id="model-search-input"
						bind:value={searchValue}
						class="w-full text-sm bg-transparent outline-none"
						placeholder={searchPlaceholder}
						autocomplete="off"
					/>
				</div>

				<hr class="border-gray-100 dark:border-gray-800" />
			{/if} -->

			<div class="px-3 my-2 max-h-64 overflow-y-auto scrollbar-hidden">
				<button
				aria-label="model-item"
				class="flex w-full text-left font-medium line-clamp-1 select-none items-center rounded-button py-2 pl-3 pr-1.5 text-sm text-gray-700 dark:text-gray-100 outline-none transition-all duration-75 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer data-[highlighted]:bg-muted"
				on:click={() => {
					selected_collection = 'All Documents';
					handleCollectionChange()
					show = false;
				}}
			>
				All Documents
			</button>
			{#if $created_collections.length > 0}
				{#each $created_collections as collection}
					<!-- <option value={collection.collection_name}> -->
					 <div class="flex">
						<button
						aria-label="model-item"
						class="flex-none w-11/12 text-left font-medium line-clamp-1 select-none items-center rounded-button py-2 pl-3 pr-1.5 text-sm text-gray-700 dark:text-gray-100 outline-none transition-all duration-75 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer data-[highlighted]:bg-muted"
						on:click={() => {
							selected_collection = collection.collection_name;
							handleCollectionChange()
							show = false;
						}}
					>
						{collection.collection_name} ({(collectionCount[collection.collection_name] || 0)} docs)
					</button>
					<button
					class="flex-none w-1/12 text-left font-medium line-clamp-1 select-none items-center rounded-button py-2 pl-3 pr-1.5 text-sm text-gray-700 dark:text-gray-100 outline-none transition-all duration-75 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer data-[highlighted]:bg-muted flex justify-center items-center"
					on:click={() => {
						handleCollectionDelete(collection.collection_name);
					}}


					>
					<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 28 24"
					stroke-width="1.5"
					stroke="currentColor"
					class="w-4 h-4"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"
					/>
				</svg>	
					</button>
					 </div>


					<!-- </option> -->
				{/each}
			{/if}

			</div>

			<div class="hidden w-[42rem]" />
			<div class="hidden w-[32rem]" />
		</slot>
	</DropdownMenu.Content>
</DropdownMenu.Root>


<style>
	input {
		display: block;
		width: 500px;
		max-width: 100%;
	}
</style>
