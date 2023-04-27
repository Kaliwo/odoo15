import { context, storage, logging, PersistentMap } from "near-sdk-as";

const purchaseOrders = new PersistentMap<string, string>("po");

export function storePurchaseOrder(poId: string, encryptedPo: string): void {
  purchaseOrders.set(poId, encryptedPo);
}

export function getPurchaseOrder(poId: string, accessKey: string): string | null {
  const encryptedPo = purchaseOrders.get(poId);
  if (encryptedPo) {
    return encryptedPo;
  }
  return null;
}
