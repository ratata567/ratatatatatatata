<script lang="ts">
	import { toast } from 'svelte-sonner';
	import dayjs from 'dayjs';
	import { onMount, getContext } from 'svelte';

	import { getDocs, tagDocByName, updateDocByName } from '$lib/apis/documents';
	import { createNewColleciton, getCollections } from '$lib/apis/collections';
	import Modal from '../common/Modal.svelte';
	import { documents } from '$lib/stores';
	import TagInput from '../common/Tags/TagInput.svelte';
	import Tags from '../common/Tags.svelte';
	import { addTagById } from '$lib/apis/chats';
	import {created_collections } from '$lib/stores';


	const i18n = getContext('i18n');

	export let show = false;
	export let selectedDoc;

	let tags = [];
	let selectedCollection = null;
	let customCollection = '';
	let collections = [];
	let showCustomInput = false;

	let doc = {
		name: '',
		title: '',
		collection_name :'',
		content: null
	};

	$:{
		created_collections.subscribe(currentItems => {
			if (currentItems.length > 0) {
			console.log(typeof currentItems)
      collections = currentItems.map(item => item.collection_name);
			}	
		});
		console.log(collections)

	}

	const submitHandler = async () => {
		if(selectedCollection == customCollection)
			{console.log("Here")
			createNewColleciton(localStorage.token, customCollection)
	}
		const res = await updateDocByName(localStorage.token, selectedDoc.name, {
			title: doc.title,
			name: doc.name,
			collection_name : selectedCollection
		}).catch((error) => {
			toast.error(error);
		});

		if (res) {
			show = false;

			await documents.set(await getDocs(localStorage.token));
			await created_collections.set( await getCollections(localStorage.token));
		}
	};

	const addTagHandler = async (tagName) => {
		if (!tags.find((tag) => tag.name === tagName) && tagName !== '') {
			tags = [...tags, { name: tagName }];

			await tagDocByName(localStorage.token, doc.name, {
				name: doc.name,
				tags: tags
			});

			documents.set(await getDocs(localStorage.token));
		} else {
			console.log('tag already exists');
		}
	};

	const deleteTagHandler = async (tagName) => {
		tags = tags.filter((tag) => tag.name !== tagName);

		await tagDocByName(localStorage.token, doc.name, {
			name: doc.name,
			tags: tags
		});

		documents.set(await getDocs(localStorage.token));
	};

	function handleSelection(event) {
    const value = event.target.value;
    if (value === 'NewCollection') {
      showCustomInput = true;
    } else {
      showCustomInput = false;
      selectedCollection = value;
    }
  	}

	function addCustomCollection() {
		if (customCollection.trim()) {
		collections = [...collections, customCollection];
		selectedCollection = customCollection;
		customCollection = '';
		showCustomInput = false;
		}
	}
	function setCustomCollection(){
		selectedCollection = customCollection
		console.log(selectedCollection)
	}

	onMount(() => {
		console.log(selectedDoc)
		if (selectedDoc) {
			doc = JSON.parse(JSON.stringify(selectedDoc));
			selectedCollection = doc.collection_name;
			tags = doc?.content?.tags ?? [];
		}
	});


</script>

<Modal size="sm" bind:show>
	<div>
		<div class=" flex justify-between dark:text-gray-300 px-5 pt-4">
			<div class=" text-lg font-medium self-center">{$i18n.t('Edit Doc')}</div>
			<button
				class="self-center"
				on:click={() => {
					show = false;
				}}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					class="w-5 h-5"
				>
					<path
						d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
					/>
				</svg>
			</button>
		</div>
		<div class="flex flex-col md:flex-row w-full px-5 py-4 md:space-x-4 dark:text-gray-200">
			<div class=" flex flex-col w-full sm:flex-row sm:justify-center sm:space-x-6">
				<form
					class="flex flex-col w-full"
					on:submit|preventDefault={() => {
						submitHandler();
					}}
				>
					<div class=" flex flex-col space-y-1.5">
						<div class="flex flex-col w-full">
							<div class=" mb-1 text-xs text-gray-500">{$i18n.t('Name Tag')}</div>

							<div class="flex flex-1">
								<div
									class="bg-gray-200 dark:bg-gray-800 font-semibold px-3 py-0.5 border border-r-0 dark:border-gray-800 rounded-l-xl flex items-center"
								>
									#
								</div>
								<input
									class="w-full rounded-r-xl py-2 px-4 text-sm dark:text-gray-300 dark:bg-gray-850 disabled:text-gray-500 dark:disabled:text-gray-500 outline-none"
									type="text"
									bind:value={doc.name}
									autocomplete="off"
									required
								/>
							</div>
						</div>

						<div class="flex flex-col w-full">
							<div class=" mb-1 text-xs text-gray-500">{$i18n.t('Title')}</div>

							<div class="flex-1">
								<input
									class="w-full rounded-xl py-2 px-4 text-sm dark:text-gray-300 dark:bg-gray-850 outline-none"
									type="text"
									bind:value={doc.title}
									autocomplete="off"
									required
								/>
							</div>
						</div>

						<div class="flex flex-col w-full">
							<div class=" mb-2 text-xs text-gray-500">{$i18n.t('Collection')}</div>
	
							<div class="flex-1 mb-1 text-m text-gray-500">
								<!-- <label for="dropdown">Choose an option:</label> -->
								<select id="dropdown"  class = "w-7/12 rounded-xl py-2 px-4 text-sm dark:text-gray-300 dark:bg-gray-850 outline-none" on:change={handleSelection} bind:value={selectedCollection}>

									<option value={doc.collection_name} selected>{doc.collection_name}</option>
									{#each collections as collection}
									{#if collection !== doc.collection_name}
									<option value={collection}>{collection}</option>
									{/if}
									{/each}
									<option value="NewCollection">+ New Collection</option>
								</select>
							</div>
							<div class="flex-1 mb-1 text-m text-gray-500">	
								{#if showCustomInput}
									<div class="flex-1 mb-1 text-m text-gray-500">
									<input 
										type="text" 
										class = "w-7/12 rounded-xl py-2 px-4 text-sm dark:text-gray-300 dark:bg-gray-850 outline-none"
										placeholder="Collection Name" 
										bind:value={customCollection}
										on:input ={setCustomCollection} 
									/>
									<!-- <button on:click={addCustomCollection}>Add</button> -->
									</div>
								{/if}
							</div>
						</div>

						<div class="flex flex-col w-full">
							<div class=" mb-3 text-xs text-gray-500">{$i18n.t('Tags')}</div>

							<Tags {tags} addTag={addTagHandler} deleteTag={deleteTagHandler} />
						</div>
					</div>

					<div class="flex justify-end pt-5 text-sm font-medium">
						<button
							class=" px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-gray-100 transition rounded-lg"
							type="submit"
						>
							{$i18n.t('Save')}
						</button>
					</div>
				</form>
			</div>
		</div>
	</div>
</Modal>

<style>
	input::-webkit-outer-spin-button,
	input::-webkit-inner-spin-button {
		/* display: none; <- Crashes Chrome on hover */
		-webkit-appearance: none;
		margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
	}

	.tabs::-webkit-scrollbar {
		display: none; /* for Chrome, Safari and Opera */
	}

	.tabs {
		-ms-overflow-style: none; /* IE and Edge */
		scrollbar-width: none; /* Firefox */
	}

	input[type='number'] {
		-moz-appearance: textfield; /* Firefox */
	}
</style>
