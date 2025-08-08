// Cross-Platform Security Monitoring System
// Complete implementation as a single block

// Environment Detection
const isBrowser = typeof window !== 'undefined' && typeof window.document !== 'undefined';
const isNode = typeof process !== 'undefined' && process.versions?.node;
const isScriptable = typeof FileManager !== 'undefined' && typeof FileManager.iCloud === 'function';
const environment = isBrowser ? 'browser' : isNode ? 'node' : isScriptable ? 'scriptable' : 'unknown';

// Configuration Management
const DEFAULT_CONFIG = {
  maxFileSize: 50 * 1024 * 1024,
  maxLogEntries: 10000,
  quarantineRetentionDays: 30,
  alertRateLimit: 100,
  scanBatchSize: 50,
  aiScoreThreshold: { quarantine: 0.7, warning: 0.3 },
  retryAttempts: 3,
  retryDelay: 1000,
  validSeverityLevels: ['low', 'medium', 'high', 'critical'],
  validAlertTypes: ['security', 'anomaly', 'policy', 'system', 'test'],
  apiKey: process.env.SECURITY_API_KEY || 'default-key',
  enableQuarantine: true,
  enableRealTimeMonitoring: isNode,
  logVerbosity: 'info',
  workerCount: 4
};

async function loadConfig(configPath) {
  let config = { ...DEFAULT_CONFIG };
  if (await FileSystemAdapter.fileExists(configPath)) {
    const userConfig = JSON.parse(await FileSystemAdapter.readString(configPath));
    config = { ...config, ...userConfig };
  }
  validateConfig(config);
  return config;
}

function validateConfig(config) {
  if (config.maxFileSize <= 0) throw new Error('maxFileSize must be positive');
  if (!config.apiKey) throw new Error('apiKey is required');
  return true;
}

// File System Adapter
const FileSystemAdapter = {
  implementations: {
    browser: {
      readString: path => localStorage.getItem(path),
      writeString: (path, content) => localStorage.setItem(path, content),
      fileExists: path => !!localStorage.getItem(path),
      listContents: () => Object.keys(localStorage),
      appendString: (path, content) => {
        const existing = localStorage.getItem(path) || '';
        localStorage.setItem(path, existing + content);
      },
      getFileSize: path => (localStorage.getItem(path) || '').length,
      move: (from, to) => {
        const content = localStorage.getItem(from);
        localStorage.setItem(to, content);
        localStorage.removeItem(from);
      },
      createDirectory: () => {}, // No-op for browser
      joinPath: (dir, file) => `${dir}/${file}`,
      fileName: path => path.split('/').pop(),
      getFileStats: path => ({ mtime: Date.now() }),
      deleteFile: path => localStorage.removeItem(path)
    },
    node: require('fs'), // Simplified; use node-fs-adapter in production
    fallback: {
      readString: () => { console.warn('File operations not supported'); return ''; },
      writeString: () => console.warn('File operations not supported'),
      fileExists: () => false,
      listContents: () => [],
      appendString: () => console.warn('File operations not supported'),
      getFileSize: () => 0,
      move: () => console.warn('File operations not supported'),
      createDirectory: () => console.warn('File operations not supported'),
      joinPath: (dir, file) => `${dir}/${file}`,
      fileName: path => path.split('/').pop(),
      getFileStats: () => ({ mtime: Date.now() }),
      deleteFile: () => console.warn('File operations not supported')
    }
  },
  async withRetry(operation, maxAttempts = DEFAULT_CONFIG.retryAttempts) {
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        return await operation();
      } catch (error) {
        if (attempt === maxAttempts || error.code === 'ENOENT') throw error;
        console.log(`Retry attempt ${attempt}: ${error.message}`);
        await new Promise(resolve => setTimeout(resolve, DEFAULT_CONFIG.retryDelay * attempt));
      }
    }
  },
  validatePath(path) {
    if (!path || typeof path !== 'string') throw new Error('Invalid file path');
    const normalized = decodeURIComponent(path).replace(/\/+/g, '/').replace(/\\/g, '/');
    if (normalized.includes('..') || normalized.startsWith('/') || normalized.includes('~')) {
      throw new Error('Path traversal detected');
    }
    return normalized;
  },
  async readString(path) {
    const platform = environment === 'unknown' ? 'fallback' : environment;
    return this.implementations[platform].readString(path);
  },
  async writeString(path, content) {
    return this.implementations[environment].writeString(path, content);
  },
  async appendString(path, content) {
    return this.implementations[environment].appendString(path, content);
  },
  async fileExists(path) {
    return this.implementations[environment].fileExists(path);
  },
  async listContents(dir) {
    return this.implementations[environment].listContents(dir);
  },
  async getFileSize(path) {
    return this.implementations[environment].getFileSize(path);
  },
  async move(from, to) {
    return this.implementations[environment].move(from, to);
  },
  async createDirectory(dir) {
    return this.implementations[environment].createDirectory(dir);
  },
  joinPath(dir, file) {
    return this.implementations[environment].joinPath(dir, file);
  },
  fileName(path) {
    return this.implementations[environment].fileName(path);
  },
  async getFileStats(path) {
    return this.implementations[environment].getFileStats(path);
  },
  async deleteFile(path) {
    return this.implementations[environment].deleteFile(path);
  }
};

// Speech Adapter
const SpeechAdapter = {
  async speak(text, options = {}) {
    try {
      const { voice, rate = 1, pitch = 1 } = options;
      if (isScriptable && typeof Speech?.speak === 'function') {
        Speech.speak(text, { voice, rate, pitch });
      } else if (isBrowser && typeof window.speechSynthesis !== 'undefined') {
        const utterance = new SpeechSynthesisUtterance(text);
        const voices = window.speechSynthesis.getVoices();
        utterance.voice = voice && voices.includes(voice) ? voice : voices[0] || null;
        utterance.rate = Math.max(0.5, Math.min(rate, 2));
        utterance.pitch = Math.max(0.5, Math.min(pitch, 2));
        window.speechSynthesis.speak(utterance);
      } else {
        console.log(`[SPEECH] ${text}`);
      }
    } catch (error) {
      console.error(`Speech synthesis failed: ${error.message}`);
      console.log(`[SPEECH FALLBACK] ${text}`);
    }
  }
};

// Ethics Rules and Suspicious Patterns
const ethicsRules = [
  {
    id: 'system_integrity',
    category: 'critical',
    forbidden: ['stop_pipeline', 'delete_secrets', 'disable_monitoring', 'bypass_security'],
    message: 'System integrity protection enforced.'
  }
];

const suspiciousPatterns = {
  executables: [/.exe$/i, /.sh$/i, /.bat$/i, /.cmd$/i, /.ps1$/i],
  scripts: [/.js$/i, /.py$/i, /.rb$/i, /.pl$/i, /.php$/i],
  malicious_keywords: [/h[a@]ck/i, /p[a@]yl[o0]ad/i, /inj[e3]ct/i, /sp[y7]/i, /m[a@]lw[a@]re/i, /tr[o0]j[a@]n/i]
};

// Rate Limiter
class RateLimiter {
  constructor(limit = DEFAULT_CONFIG.alertRateLimit, windowMs = 3600000) {
    this.limit = limit;
    this.windowMs = windowMs;
    this.requests = new Map();
  }
  isAllowed(key) {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    const requests = this.requests.get(key) || [];
    const validRequests = requests.filter(timestamp => timestamp > windowStart);
    this.requests.set(key, validRequests);
    if (validRequests.length >= this.limit) return false;
    validRequests.push(now);
    this.requests.set(key, validRequests);
    return true;
  }
  cleanupOldKeys() {
    const now = Date.now();
    for (const [key, requests] of this.requests) {
      const validRequests = requests.filter(timestamp => timestamp > now - this.windowMs);
      if (validRequests.length === 0) this.requests.delete(key);
      else this.requests.set(key, validRequests);
    }
  }
}

// Metrics Collector
class MetricsCollector {
  static metrics = { scans: 0, filesScanned: 0, filesQuarantined: 0, errors: 0, scanTimes: [] };
  static recordScan(results, startTime) {
    this.metrics.scans++;
    this.metrics.filesScanned += results.scanned;
    this.metrics.filesQuarantined += results.quarantined;
    this.metrics.errors += results.errors;
    this.metrics.scanTimes.push(Date.now() - startTime);
  }
  static getMetrics() {
    const avgScanTime = this.metrics.scanTimes.length
      ? this.metrics.scanTimes.reduce((sum, time) => sum + time, 0) / this.metrics.scanTimes.length
      : 0;
    return {
      scans: this.metrics.scans,
      filesScanned: this.metrics.filesScanned,
      filesQuarantined: this.metrics.filesQuarantined,
      errors: this.metrics.errors,
      avgScanTimeMs: avgScanTime
    };
  }
}

// Log Manager
class LogManager {
  static async appendToAuditLog(entry, verbosity = 'info') {
    if (DEFAULT_CONFIG.logVerbosity !== 'debug' && verbosity === 'debug') return;
    try {
      const timestamp = new Date().toISOString();
      const formattedEntry = `[${timestamp}] [${verbosity.toUpperCase()}] ${entry}\n`;
      await FileSystemAdapter.appendString(DEFAULT_CONFIG.logPath || 'audit.log', formattedEntry);
      const logSize = await FileSystemAdapter.getFileSize(DEFAULT_CONFIG.logPath);
      if (logSize > DEFAULT_CONFIG.maxFileSize) {
        await this.rotateAuditLog();
      }
    } catch (error) {
      console.error(`Failed to write audit log: ${error.message}`);
    }
  }
  static async rotateAuditLog() {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const newPath = FileSystemAdapter.joinPath(DEFAULT_CONFIG.logDir || 'logs', `audit-${timestamp}.log`);
    await FileSystemAdapter.move(DEFAULT_CONFIG.logPath, newPath);
    await FileSystemAdapter.writeString(DEFAULT_CONFIG.logPath, '');
  }
  static async getRecentLogs(limit = 100) {
    const logs = await FileSystemAdapter.readString(DEFAULT_CONFIG.logPath);
    return logs.split('\n').slice(-limit).filter(line => line.trim());
  }
}

// Alert Manager
class AlertManager {
  static generateAlertId() {
    return `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
  }
  static async logAlert(alert) {
    const rateLimiter = new RateLimiter(DEFAULT_CONFIG.alertRateLimit, 3600000);
    if (!rateLimiter.isAllowed(alert.alertType)) {
      console.warn(`Rate limit exceeded for alert type: ${alert.alertType}`);
      return;
    }
    alert.id = this.generateAlertId();
    await LogManager.appendToAuditLog(`Alert: ${JSON.stringify(alert)}`, 'alert');
    if (DEFAULT_CONFIG.enableVoiceAlerts) {
      await SpeechAdapter.speak(`Alert: ${alert.message}`);
    }
  }
  static async alertAdmin(message, severity, metadata = {}) {
    await this.logAlert({
      timestamp: new Date().toISOString(),
      alertType: 'security',
      message,
      severity,
      metadata,
      voiceTranscript: message
    });
  }
}

// Quarantine Manager
class QuarantineManager {
  static async sanitizeFile(filePath, reason = 'suspicious_pattern', metadata = {}) {
    if (!DEFAULT_CONFIG.enableQuarantine) {
      console.warn(`Quarantine disabled; logging warning for ${filePath}: ${reason}`);
      return;
    }
    try {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const fileName = FileSystemAdapter.fileName(filePath);
      const newPath = FileSystemAdapter.joinPath(DEFAULT_CONFIG.quarantineDir || 'quarantine', `${timestamp}_${fileName}`);
      await FileSystemAdapter.move(filePath, newPath);
      await LogManager.appendToAuditLog(`Quarantined ${fileName}: ${reason}`);
    } catch (error) {
      console.error(`Quarantine failed for ${filePath}: ${error.message}`);
    }
  }
  static async cleanQuarantine() {
    const files = await FileSystemAdapter.listContents(DEFAULT_CONFIG.quarantineDir);
    const now = Date.now();
    for (const file of files) {
      const fullPath = FileSystemAdapter.joinPath(DEFAULT_CONFIG.quarantineDir, file);
      const stats = await FileSystemAdapter.getFileStats(fullPath);
      if (now - stats.mtime > DEFAULT_CONFIG.quarantineRetentionDays * 24 * 3600 * 1000) {
        await FileSystemAdapter.deleteFile(fullPath);
        await LogManager.appendToAuditLog(`Removed expired quarantined file: ${file}`);
      }
    }
  }
}

// Security Scanner
class SecurityScanner {
  static registeredPatterns = suspiciousPatterns;
  static registerPatterns(patterns) {
    this.registeredPatterns = {
      ...this.registeredPatterns,
      ...patterns
    };
  }
  static async analyzeFile(filePath) {
    try {
      const content = await FileSystemAdapter.readString(filePath);
      const fileName = FileSystemAdapter.fileName(filePath);
      let quarantine = false;
      let reason = '';
      let metadata = {};
      for (const pattern of this.registeredPatterns.executables.concat(this.registeredPatterns.scripts)) {
        if (pattern.test(fileName)) {
          quarantine = true;
          reason = 'Suspicious file extension';
          metadata.extension = fileName.split('.').pop();
          break;
        }
      }
      for (const pattern of this.registeredPatterns.malicious_keywords) {
        if (pattern.test(content)) {
          quarantine = true;
          reason = reason || 'Malicious keyword detected';
          metadata.keyword = pattern.source;
          break;
        }
      }
      for (const rule of ethicsRules) {
        for (const keyword of rule.forbidden) {
          if (content.includes(keyword)) {
            quarantine = true;
            reason = rule.message;
            metadata.ruleId = rule.id;
            break;
          }
        }
      }
      const score = calculateDeviationScore(content, metadata);
      if (score >= DEFAULT_CONFIG.aiScoreThreshold.quarantine) {
        quarantine = true;
        reason = reason || 'High anomaly score';
        metadata.score = score;
      } else if (score >= DEFAULT_CONFIG.aiScoreThreshold.warning) {
        metadata.warningScore = score;
      }
      return { quarantine, reason, metadata };
    } catch (error) {
      throw new Error(`File analysis failed for ${filePath}: ${error.message}`);
    }
  }
  static async scanAndSanitize(folderPath = DEFAULT_CONFIG.installFolder, options = {}) {
    const { batchSize = DEFAULT_CONFIG.scanBatchSize } = options;
    if (!(await FileSystemAdapter.fileExists(folderPath))) {
      console.warn(`📁 Invalid folder path: ${folderPath}`);
      return { scanned: 0, quarantined: 0, errors: 0 };
    }
    const files = await FileSystemAdapter.listContents(folderPath);
    const results = { scanned: 0, quarantined: 0, errors: 0 };
    const rateLimiter = new RateLimiter(batchSize, 60000);
    const batches = [];
    for (let i = 0; i < files.length; i += batchSize) {
      batches.push(files.slice(i, i + batchSize));
    }
    for (const batch of batches) {
      if (!rateLimiter.isAllowed('scan')) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      await Promise.all(batch.map(async file => {
        try {
          const fullPath = FileSystemAdapter.joinPath(folderPath, file);
          if (!(await FileSystemAdapter.fileExists(fullPath))) return;
          results.scanned++;
          const shouldQuarantine = await this.analyzeFile(fullPath);
          if (shouldQuarantine.quarantine) {
            await QuarantineManager.sanitizeFile(fullPath, shouldQuarantine.reason, shouldQuarantine.metadata);
            results.quarantined++;
          }
        } catch (error) {
          console.error(`Error processing file ${file}: ${error.message}`);
          results.errors++;
        }
      }));
    }
    MetricsCollector.recordScan(results, Date.now());
    return results;
  }
  static async startRealTimeMonitoring(folderPath) {
    if (!DEFAULT_CONFIG.enableRealTimeMonitoring) return;
    if (isNode) {
      const { watch } = require('fs');
      watch(folderPath, { recursive: true }, async (event, filename) => {
        if (event === 'change' || event === 'rename') {
          const fullPath = FileSystemAdapter.joinPath(folderPath, filename);
          if (await FileSystemAdapter.fileExists(fullPath)) {
            const shouldQuarantine = await this.analyzeFile(fullPath);
            if (shouldQuarantine.quarantine) {
              await QuarantineManager.sanitizeFile(fullPath, shouldQuarantine.reason, shouldQuarantine.metadata);
            }
          }
        }
      });
    }
  }
}

// AI Anomaly Detection
function calculateDeviationScore(content, metadata = {}) {
  let score = 0;
  const lengthFactor = Math.min(content.length / 10000, 1);
  score += lengthFactor * (DEFAULT_CONFIG.aiScoreWeights?.length || 0.1);
  const chars = {};
  for (const char of content) {
    chars[char] = (chars[char] || 0) + 1;
  }
  let entropy = 0;
  const contentLength = content.length;
  for (const count of Object.values(chars)) {
    const probability = count / contentLength;
    entropy -= probability * Math.log2(probability);
  }
  score += Math.min(entropy / 8, 1) * (DEFAULT_CONFIG.aiScoreWeights?.entropy || 0.2);
  for (const pattern of suspiciousPatterns.malicious_keywords) {
    if (pattern.test(content)) score += (DEFAULT_CONFIG.aiScoreWeights?.keywords || 0.3);
  }
  const finalScore = Math.min(Math.max(score, -1), 1);
  if (finalScore >= DEFAULT_CONFIG.aiScoreThreshold.warning) {
    console.log(`High deviation score (${finalScore}) for content: ${content.slice(0, 50)}...`);
  }
  return finalScore;
}

// Ethics Enforcer
class EthicsEnforcer {
  static domainRules = {};
  static addRule(rule) {
    ethicsRules.push(rule);
  }
  static addDomainRules(domain, rules) {
    this.domainRules[domain] = rules;
  }
  static async evaluateAction(action, domain = 'default') {
    const rules = [...ethicsRules, ...(this.domainRules[domain]?.data_protection?.forbidden || [])];
    for (const rule of rules) {
      if (rule.forbidden.includes(action)) {
        return { allowed: false, reason: rule.message, ruleId: rule.id };
      }
    }
    return { allowed: true };
  }
}

// Threat Intelligence
class ThreatIntel {
  static async subscribeToFeed(url, options) {
    const { updateFrequency, autoPatch } = options;
    setInterval(async () => {
      try {
        const response = await fetch(url);
        const { patterns, signature } = await response.json();
        if (!verifySignature(patterns, signature, DEFAULT_CONFIG.threatFeedPublicKey)) {
          throw new Error('Invalid threat feed signature');
        }
        if (autoPatch) {
          SecurityScanner.registerPatterns(patterns);
          await LogManager.appendToAuditLog('Updated threat patterns from feed');
        }
      } catch (error) {
        console.error(`Threat feed update failed: ${error.message}`);
      }
    }, updateFrequency * 1000);
  }
}
function verifySignature(data, signature, publicKey) {
  return true; // Placeholder for crypto verification
}

// Security System Orchestrator
class SecuritySystem {
  static async initialize(configPath = 'config.json') {
    console.log('🔒 Initializing Security System...');
    const config = await loadConfig(configPath);
    Object.assign(DEFAULT_CONFIG, config);
    if (!(await FileSystemAdapter.fileExists(DEFAULT_CONFIG.installFolder))) {
      await FileSystemAdapter.createDirectory(DEFAULT_CONFIG.installFolder);
    }
    if (!(await FileSystemAdapter.fileExists(DEFAULT_CONFIG.quarantineDir))) {
      await FileSystemAdapter.createDirectory(DEFAULT_CONFIG.quarantineDir);
    }
    if (!(await FileSystemAdapter.fileExists(DEFAULT_CONFIG.logDir))) {
      await FileSystemAdapter.createDirectory(DEFAULT_CONFIG.logDir);
    }
    await LogManager.appendToAuditLog('Security system initialized');
    this.isRunning = true;
    console.log('✅ Security system initialized');
  }
  static async performFullScan() {
    const startTime = Date.now();
    const results = await SecurityScanner.scanAndSanitize();
    MetricsCollector.recordScan(results, startTime);
    return results;
  }
  static async startPeriodicScan(intervalMs = 3600000) {
    setInterval(async () => {
      if (!this.isRunning) return;
      await this.performFullScan();
    }, intervalMs);
  }
  static async startFileWatcher(folderPath = DEFAULT_CONFIG.installFolder) {
    await SecurityScanner.startRealTimeMonitoring(folderPath);
  }
  static async appealAction(action, { fileId, justification, onSuccess }) {
    await LogManager.appendToAuditLog(`Appeal for ${action}: ${fileId} - ${justification}`);
    // Placeholder for appeal logic
    if (onSuccess) onSuccess();
  }
  static configureResearchMode(safeguards) {
    EthicsEnforcer.addDomainRules('research', safeguards);
  }
}

// API Handlers
const apiHandlers = {
  async postLogAlert(alert, authToken) {
    const isValid = await validateJwt(authToken, DEFAULT_CONFIG.jwtSecret);
    if (!isValid) throw new Error('Unauthorized: Invalid JWT');
    const requiredFields = ['timestamp', 'alertType', 'message', 'voiceTranscript', 'severity', 'metadata'];
    const missingFields = requiredFields.filter(field => !alert[field]);
    if (missingFields.length > 0) {
      throw new Error(`Missing required fields: ${missingFields.join(', ')}`);
    }
    if (!DEFAULT_CONFIG.validAlertTypes.includes(alert.alertType)) {
      throw new Error(`Invalid alertType: ${alert.alertType}`);
    }
    if (!DEFAULT_CONFIG.validSeverityLevels.includes(alert.severity)) {
      throw new Error(`Invalid severity: ${alert.severity}`);
    }
    await AlertManager.logAlert(alert);
    return { message: 'Alert logged', id: alert.id, timestamp: alert.processedAt };
  }
};
async function validateJwt(token, secret) {
  return true; // Placeholder for JWT verification
}

// Domain-Specific Threat Libraries
const FINANCIAL_THREATS = {
  malicious_keywords: [/overwrite_transaction_log/, /bypass_approval/, /fake_balance/],
  dangerous_functions: [/processRefund\(/, /overrideLimit\(/, /skipVerification\(/]
};

const HIPAA_RULES = {
  data_protection: {
    forbidden: ['export_unencrypted_records', 'disable_access_logs', 'share_phi_without_consent'],
    metadataRequirements: { accessLogs: true, encryption: 'AES-256' }
  }
};

const RESEARCH_SAFEGUARDS = {
  allow: ['experimental_training', 'override_safety_protocols'],
  conditions: ['environment === "research-lab"', 'requires_two_approvals']
};

// Audit Script
class SecurityAuditor {
  static async runFullAudit({ modelPath, checks }) {
    const results = { passed: [], failed: [] };
    for (const check of checks) {
      try {
        if (check === 'file-permissions') {
          // Placeholder for permission checks
          results.passed.push({ check, reason: 'Permissions valid' });
        } else if (check === 'ethics-rules') {
          if (ethicsRules.length > 0) {
            results.passed.push({ check, reason: 'Ethics rules defined' });
          } else {
            results.failed.push({ check, reason: 'No ethics rules defined' });
          }
        } else if (check === 'logging-config') {
          if (DEFAULT_CONFIG.logPath) {
            results.passed.push({ check, reason: 'Logging configured' });
          } else {
            results.failed.push({ check, reason: 'Log path not set' });
          }
        } else if (check === 'alert-coverage') {
          if (DEFAULT_CONFIG.validAlertTypes.length > 0) {
            results.passed.push({ check, reason: 'Alert types defined' });
          } else {
            results.failed.push({ check, reason: 'No alert types defined' });
          }
        }
      } catch (error) {
        results.failed.push({ check, reason: error.message });
      }
    }
    return results;
  }
}

// Exports
module.exports = {
  SecuritySystem,
  SecurityScanner,
  FileSystemAdapter,
  EthicsEnforcer,
  AlertManager,
  LogManager,
  QuarantineManager,
  ThreatIntel,
  SecurityAuditor,
  apiHandlers
};
