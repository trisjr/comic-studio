// AI Coding
/**
 * @file s3-object-storage.adapter.ts
 * @description Hien thuc `ObjectStoragePort` bang tap con S3. Cung mot adapter
 * chay voi MinIO o may dev va voi vendor S3-compatible o production (ADR-004).
 */

import {
  CopyObjectCommand,
  DeleteObjectCommand,
  GetObjectCommand,
  HeadObjectCommand,
  PutObjectCommand,
  S3Client,
} from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

import type { StorageEnv } from '../config/env';
import type {
  ObjectKey,
  ObjectMetadata,
  ObjectStoragePort,
  PutObjectInput,
  SignedUrl,
} from './object-storage.port';

const NOT_FOUND_STATUS = 404;

export class S3ObjectStorageAdapter implements ObjectStoragePort {
  private readonly client: S3Client;

  constructor(private readonly env: StorageEnv) {
    this.client = new S3Client({
      endpoint: env.STORAGE_ENDPOINT,
      region: env.STORAGE_REGION,
      forcePathStyle: env.STORAGE_FORCE_PATH_STYLE,
      credentials: {
        accessKeyId: env.STORAGE_ACCESS_KEY_ID,
        secretAccessKey: env.STORAGE_SECRET_ACCESS_KEY,
      },
    });
  }

  async put({ key, body, contentType }: PutObjectInput): Promise<void> {
    await this.client.send(
      new PutObjectCommand({
        Bucket: this.env.STORAGE_BUCKET,
        Key: key,
        Body: body,
        ContentType: contentType,
      }),
    );
  }

  async get(key: ObjectKey): Promise<Uint8Array> {
    const result = await this.client.send(
      new GetObjectCommand({ Bucket: this.env.STORAGE_BUCKET, Key: key }),
    );

    if (result.Body === undefined) {
      throw new Error(`Object "${key}" khong co noi dung`);
    }

    return result.Body.transformToByteArray();
  }

  async head(key: ObjectKey): Promise<ObjectMetadata | undefined> {
    try {
      const result = await this.client.send(
        new HeadObjectCommand({ Bucket: this.env.STORAGE_BUCKET, Key: key }),
      );

      return {
        key,
        sizeInBytes: result.ContentLength ?? 0,
        contentType: result.ContentType,
      };
    } catch (error) {
      if (isNotFound(error)) {
        return undefined;
      }
      throw error;
    }
  }

  async copy(sourceKey: ObjectKey, destinationKey: ObjectKey): Promise<void> {
    await this.client.send(
      new CopyObjectCommand({
        Bucket: this.env.STORAGE_BUCKET,
        CopySource: `${this.env.STORAGE_BUCKET}/${sourceKey}`,
        Key: destinationKey,
      }),
    );
  }

  /**
   * ADR-004 dieu 8: credential cua `api` va `worker` KHONG duoc co quyen xoa tren
   * prefix canonical. Phuong thuc nay ton tai cho duong dac quyen hard-delete
   * tenant va cho viec don prefix `incoming/` sau khi upload hai pha hoan tat.
   */
  async delete(key: ObjectKey): Promise<void> {
    await this.client.send(
      new DeleteObjectCommand({ Bucket: this.env.STORAGE_BUCKET, Key: key }),
    );
  }

  async presignGet(key: ObjectKey): Promise<SignedUrl> {
    return getSignedUrl(
      this.client,
      new GetObjectCommand({ Bucket: this.env.STORAGE_BUCKET, Key: key }),
      { expiresIn: this.env.STORAGE_SIGNED_URL_TTL_SECONDS },
    );
  }

  async presignPut(key: ObjectKey, contentType: string): Promise<SignedUrl> {
    return getSignedUrl(
      this.client,
      new PutObjectCommand({
        Bucket: this.env.STORAGE_BUCKET,
        Key: key,
        ContentType: contentType,
      }),
      { expiresIn: this.env.STORAGE_SIGNED_URL_TTL_SECONDS },
    );
  }
}

const isNotFound = (error: unknown): boolean =>
  typeof error === 'object' &&
  error !== null &&
  '$metadata' in error &&
  (error as { $metadata?: { httpStatusCode?: number } }).$metadata?.httpStatusCode ===
    NOT_FOUND_STATUS;
