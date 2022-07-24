import requests
import pandas as pd
import tqdm

def get_nfts_from_collection(contract_addres, token_id):
	api_key = 'wsolaA7GgR1JjQmFyWL8di7UNm3iryQ2'
	base_url = f'https://eth-mainnet.alchemyapi.io/nft/v2/{api_key}/getNFTsForCollection'
	with_metadata = 'true'
	url = f'{base_url}?contractAddress={contract_addres}&startToken={token_id}&withMetadata={with_metadata}'
	response = requests.get(url)
	all_colletion_nfts_attributes = []
	global has_next_page
	try:
		response.json()['nextToken']
		for i in range(0, len(response.json()['nfts'])):
			all_colletion_nfts_attributes.append(response.json()['nfts'][i]['metadata']['attributes'])
		return all_colletion_nfts_attributes
	except KeyError:
		has_next_page = False
		for i in range(0, len(response.json()['nfts'])):
			all_colletion_nfts_attributes.append(response.json()['nfts'][i]['metadata']['attributes'])
		return all_colletion_nfts_attributes

# def get_nft_traits(all_nfts):

def get_collection_traits(all_colletion_nfts_attributes):
	nft_collection_traits = []
	for i in all_colletion_nfts_attributes[0]:
		nft_collection_traits.append(i['trait_type'])
	return nft_collection_traits

def get_rarity_percentage_for_attributes(all_nfts, collection_traits):
	df = pd.DataFrame([], columns=collection_traits)

	#Собрали все атрибуты, записали в датафрейм
	for i in range(0, len(all_nfts)):
		for j in range(0, len(all_nfts[i])):
			nft_traits = {}
			for k in range(0, len(all_nfts[0][j])):
				nft_traits[f"{all_nfts[0][j][k]['trait_type']}"] = all_nfts[0][j][k]['value']
			ser = pd.DataFrame([nft_traits], columns = collection_traits)
			df = pd.concat([df, ser])

	rarity_df = pd.DataFrame([])
	for column in collection_traits:
		s = pd.Series(df[column]).value_counts(normalize=True)
		rarity_df = pd.concat([rarity_df, s], axis=1)
	return rarity_df

all_nfts = []
has_next_page = True
start_token_id = 0
while has_next_page:
	all_nfts.append(get_nfts_from_collection('0xC7dF86762ba83f2a6197e1Ff9Bb40ae0f696B9E6', start_token_id))
	start_token_id += 100

collection_traits = get_collection_traits(all_nfts[0])
rarity_df = get_rarity_percentage_for_attributes(all_nfts, collection_traits)



print(rarity_df)
