use rsa::{RSAPublicKey, RSAPrivateKey, PublicKey, PublicKeyEncoding, PrivateKeyEncoding};
use rsa::padding::PaddingScheme;
use rand::Rng;
use rand::rngs::OsRng;
use near_sdk::{near_bindgen, AccountId};
use near_sdk::collections::UnorderedMap;
use near_sdk::borsh::{self, BorshDeserialize, BorshSerialize};
use near_sdk::serde::{Deserialize, Serialize};

#[near_bindgen]
#[derive(BorshDeserialize, BorshSerialize)]
pub struct PurchaseOrderContract {
    key_pairs: UnorderedMap<AccountId, (Vec<u8>, Vec<u8>)>,
}

impl Default for PurchaseOrderContract {
    fn default() -> Self {
        Self {
            key_pairs: UnorderedMap::new(b"key_pairs".to_vec()),
        }
    }
}

#[derive(Serialize, Deserialize)]
pub struct EncryptedData {
    pub encrypted_data: Vec<u8>,
    pub access_key: Vec<u8>,
}

#[near_bindgen]
impl PurchaseOrderContract {
    pub fn add_key_pair(&mut self, account_id: AccountId) {
        let mut rng = OsRng;
        let private_key = RSAPrivateKey::new(&mut rng, 2048).unwrap();
        let public_key = RSAPublicKey::from(&private_key);

        self.key_pairs.insert(&account_id, &(public_key.to_pkcs1().unwrap(), private_key.to_pkcs1().unwrap()));
    }

    pub fn encrypt_purchase_order(&self, account_id: AccountId, data: String) -> Option<EncryptedData> {
        if let Some((public_key_bytes, _)) = self.key_pairs.get(&account_id) {
            let public_key = RSAPublicKey::from_pkcs1(&public_key_bytes).unwrap();
            let mut rng = OsRng;
            let padding1 = PaddingScheme::new_pkcs1v15_encrypt();
            let encrypted_data = public_key.encrypt(&mut rng, padding1, data.as_bytes()).unwrap();

            let access_key: [u8; 32] = rng.gen();
            let padding2 = PaddingScheme::new_pkcs1v15_encrypt();
            let encrypted_access_key = public_key.encrypt(&mut rng, padding2, &access_key).unwrap();

            Some(EncryptedData {
                encrypted_data,
                access_key: encrypted_access_key,
            })
        } else {
            None
        }
    }

    pub fn decrypt_purchase_order(&self, account_id: AccountId, encrypted_data: Vec<u8>, encrypted_access_key: Vec<u8>) -> Option<String> {
        if let Some((_, private_key_bytes)) = self.key_pairs.get(&account_id) {
            let private_key = RSAPrivateKey::from_pkcs1(&private_key_bytes).unwrap();
            let padding3 = PaddingScheme::new_pkcs1v15_encrypt();
            let access_key = private_key.decrypt(padding3, &encrypted_access_key).ok()?;
            let padding4 = PaddingScheme::new_pkcs1v15_encrypt();
            let decrypted_data = private_key.decrypt(padding4, &encrypted_data).ok()?;

            if access_key == decrypted_data[0..32] {
                Some(String::from_utf8(decrypted_data[32..].to_vec()).unwrap())
            } else {
                None
            }
        } else {
            None
        }
    }
}
