// AI Coding
/**
 * @file object-storage.port.ts
 * @description Hop dong ma phan con lai cua he thong duoc phep dung voi object
 * storage. ADR-004 dieu 1 gioi han o dung tap con S3 nay — doi vendor la doi
 * endpoint va credential, khong sua mot dong code nghiep vu nao.
 *
 * ⚠️ Khong them phuong thuc chi vi mot vendor co san no. Danh sach nay la ranh
 * gioi, khong phai diem khoi dau.
 */

export type ObjectKey = string;

export type PutObjectInput = {
  readonly key: ObjectKey;
  readonly body: Uint8Array;
  readonly contentType: string;
};

export type ObjectMetadata = {
  readonly key: ObjectKey;
  readonly sizeInBytes: number;
  readonly contentType: string | undefined;
};

/**
 * ADR-004 dieu 3: URL da ky KHONG BAO GIO duoc luu ben — khong vao DB, khong ra
 * log, khong nhung vao file export. No duoc sinh tai thoi diem dung response va
 * chet cung response do.
 */
export type SignedUrl = string;

export interface ObjectStoragePort {
  put(input: PutObjectInput): Promise<void>;
  get(key: ObjectKey): Promise<Uint8Array>;
  head(key: ObjectKey): Promise<ObjectMetadata | undefined>;
  copy(sourceKey: ObjectKey, destinationKey: ObjectKey): Promise<void>;
  delete(key: ObjectKey): Promise<void>;
  presignGet(key: ObjectKey): Promise<SignedUrl>;
  presignPut(key: ObjectKey, contentType: string): Promise<SignedUrl>;
}

export const OBJECT_STORAGE_PORT = Symbol('ObjectStoragePort');
