import * as openpgp from 'openpgp';

/**
 * Node Core OpenPGP provider.
 *
 * This module is intentionally protocol-neutral. Callers provide keys and
 * message material; the provider does not persist private keys or protocol state.
 */
export class OpenPGPProvider {
  async generateKey(options = {}) {
    return openpgp.generateKey(options);
  }

  async readPublicKey(armoredKey) {
    return openpgp.readKey({ armoredKey });
  }

  async readPrivateKey(armoredKey) {
    return openpgp.readPrivateKey({ armoredKey });
  }

  async decryptPrivateKey(privateKey, passphrase) {
    return openpgp.decryptKey({ privateKey, passphrase });
  }

  async encrypt({ data, encryptionKeys, signingKeys, format = 'binary' }) {
    const message = typeof data === 'string'
      ? await openpgp.createMessage({ text: data })
      : await openpgp.createMessage({ binary: data });

    return openpgp.encrypt({
      message,
      encryptionKeys,
      signingKeys,
      format
    });
  }

  async decrypt({ message, decryptionKeys, verificationKeys, format = 'binary' }) {
    const parsed = typeof message === 'string'
      ? await openpgp.readMessage({ armoredMessage: message })
      : await openpgp.readMessage({ binaryMessage: message });

    return openpgp.decrypt({
      message: parsed,
      decryptionKeys,
      verificationKeys,
      format
    });
  }

  async sign({ data, signingKeys, detached = false, format = 'armored' }) {
    const message = typeof data === 'string'
      ? await openpgp.createMessage({ text: data })
      : await openpgp.createMessage({ binary: data });

    return openpgp.sign({
      message,
      signingKeys,
      detached,
      format
    });
  }

  async verify({ message, verificationKeys, format = 'armored' }) {
    const parsed = typeof message === 'string'
      ? await openpgp.readMessage({ armoredMessage: message })
      : await openpgp.readMessage({ binaryMessage: message });

    return openpgp.verify({
      message: parsed,
      verificationKeys,
      format
    });
  }
}

export const openPGPProvider = new OpenPGPProvider();
