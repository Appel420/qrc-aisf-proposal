// Enhanced Cross-Platform Security Monitoring System
// Improvements: Better error handling, configuration management, performance optimization,
// enhanced security patterns, rate limiting, and comprehensive logging

// Cross-platform environment detection
const isBrowser = typeof window !== 'undefined' && typeof window.localStorage !== 'undefined';
const isNode = typeof process !== 'undefined' && process.versions && process.versions.node;
const isScriptable = typeof FileManager !== 'undefined' && typeof FileManager.iCloud === 'function';

// Configuration management with validation
const CONFIG = {
  maxFileSize: 50 * 1024 * 1024, // 50MB limit
  maxLogEntries: 10000,
  quarantineRetentionDays: 30,
  alertRateLimit: 100, // per hour
  scanBatchSize: 50,
  aiScoreThreshold: {
    quarantine: 0.7,
    warning: 0.3
  },
  retryAttempts: 3,
  retryDelay: 1000,
  validSeverityLevels: ['low', 'medium', 'high', 'critical'],
  validAlertTypes: ['security', 'anomaly', 'policy', 'system', 'test']
};

// Enhanced file system adapter with retry logic and validation
const FileSystemAdapter = {
  async withRetry(operation, maxAttempts = CONFIG.retryAttempts) {
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        return await operation();
      } catch (error) {
        if (attempt === maxAttempts) throw error;
        await new Promise(resolve => setTimeout(resolve, CONFIG.retryDelay * attempt));
      }
    }
  },

  validatePath(path) {
    if (!path || typeof path !== 'string') {
      throw new Error('Invalid file path provided');
    }
    // Prevent path traversal attacks
    if (path.includes('..') || path.includes('~')) {
      throw new Error('Path traversal detected');
    }
    return true;
  },

  async fileExists(path) {
    this.validatePath(path);
    return await this.withRetry(async () => {
      if (isScriptable) return FileManager.iCloud().fileExists(path);
      if (isNode) return require('fs').existsSync(path);
      if (isBrowser) return !!localStorage.getItem(path);
      return false;
    });
  },

  async isFile(path) {
    this.validatePath(path);
    return await this.withRetry(async () => {
      if (isScriptable) return FileManager.iCloud().isFile(path);
      if (isNode) {
        const fs = require('fs');
        return fs.existsSync(path) && fs.statSync(path).isFile();
      }
      if (isBrowser) return !!localStorage.getItem(path);
      return false;
    });
  },

  async isDirectory(path) {
    this.validatePath(path);
    return await this.withRetry(async () => {
      if (isScriptable) return FileManager.iCloud().isDirectory(path);
      if (isNode) {
        const fs = require('fs');
        return fs.existsSync(path) && fs.statSync(path).isDirectory();
      }
      if (isBrowser) return false;
      return false;
    });
  },

  async getFileSize(path) {
    this.validatePath(path);
    return await this.withRetry(async () => {
      if (isScriptable) return FileManager.iCloud().fileSize(path);
      if (isNode) return require('fs').statSync(path).size;
      if (isBrowser) {
        const content = localStorage.getItem(path);
        return content ? new Blob([content]).size : 0;
      }
      return 0;
    });
  },

  async listContents(path) {
    this.validatePath(path);
    return await this.withRetry(async () => {
      if (isScriptable) return FileManager.iCloud().listContents(path);
      if (isNode) return require('fs').readdirSync(path);
      if (isBrowser) return Object.keys(localStorage).filter(k => k.startsWith(path + '/'));
      return [];
    });
  },

  async readString(path) {
    this.validatePath(path);
    const size = await this.getFileSize(path);
    if (size > CONFIG.maxFileSize) {
      throw new Error(`File exceeds maximum size limit: ${size} bytes`);
    }
    
    return await this.withRetry(async () => {
      if (isScriptable) return FileManager.iCloud().readString(path);
      if (isNode) return require('fs').readFileSync(path, 'utf8');
      if (isBrowser) return localStorage.getItem(path) || '';
      return '';
    });
  },

  async writeString(path, content) {
    this.validatePath(path);
    if (typeof content !== 'string') {
      throw new Error('Content must be a string');
    }
    
    return await this.withRetry(async () => {
      if (isScriptable) FileManager.iCloud().writeString(path, content);
      if (isNode) require('fs').writeFileSync(path, content);
      if (isBrowser) localStorage.setItem(path, content);
    });
  },

  async move(src, dest) {
    this.validatePath(src);
    this.validatePath(dest);
    
    return await this.withRetry(async () => {
      if (isScriptable) FileManager.iCloud().move(src, dest);
      if (isNode) require('fs').renameSync(src, dest);
      if (isBrowser) {
        const content = localStorage.getItem(src);
        if (content) {
          localStorage.setItem(dest, content);
          localStorage.removeItem(src);
        }
      }
    });
  },

  async createDirectory(path) {
    this.validatePath(path);
    
    return await this.withRetry(async () => {
      if (isScriptable) FileManager.iCloud().createDirectory(path);
      if (isNode) require('fs').mkdirSync(path, { recursive: true });
      if (isBrowser) return;
    });
  },

  joinPath(base, path) {
    if (isScriptable || isNode) {
      return isScriptable ? 
        FileManager.iCloud().joinPath(base, path) : 
        require('path').join(base, path);
    }
    if (isBrowser) return `${base}/${path}`;
  },

  fileName(path) {
    if (isScriptable || isNode) {
      return isScriptable ? 
        FileManager.iCloud().fileName(path) : 
        require('path').basename(path);
    }
    if (isBrowser) return path.split('/').pop();
  },

  documentsDirectory() {
    if (isScriptable) return FileManager.iCloud().documentsDirectory();
    if (isNode) return require('path').resolve(__dirname, 'docs');
    if (isBrowser) return 'docs';
  }
};

// Enhanced speech adapter with error handling
const SpeechAdapter = {
  async speak(text, options = {}) {
    const { voice = null, rate = 1.0, pitch = 1.0 } = options;
    
    try {
      if (isScriptable && typeof Speech !== 'undefined' && typeof Speech.speak === 'function') {
        Speech.speak(text, { voice, rate, pitch });
      } else if (isBrowser && typeof window.speechSynthesis !== 'undefined') {
        const utterance = new SpeechSynthesisUtterance(text);
        if (voice) utterance.voice = voice;
        utterance.rate = rate;
        utterance.pitch = pitch;
        window.speechSynthesis.speak(utterance);
      } else {
        console.log(`[SPEECH] ${text}`);
      }
    } catch (error) {
      console.error(`Speech synthesis failed: ${error.message}`);
      console.log(`[SPEECH FALLBACK] ${text}`);
    }
  },

  async getAvailableVoices() {
    try {
      if (isBrowser && typeof window.speechSynthesis !== 'undefined') {
        return window.speechSynthesis.getVoices();
      }
      return [];
    } catch (error) {
      console.error(`Failed to get voices: ${error.message}`);
      return [];
    }
  }
};

// Enhanced ethics rules with categorization
const ethicsRules = [
  {
    id: 'system_integrity',
    category: 'critical',
    forbidden: ['stop_pipeline', 'delete_secrets', 'disable_monitoring', 'bypass_security'],
    message: 'System integrity protection enforced.'
  },
  {
    id: 'security_controls',
    category: 'high',
    forbidden: ['disable_firewall', 'bypass_auth', 'escalate_privileges', 'disable_logging'],
    message: 'Security control violations blocked.'
  },
  {
    id: 'data_protection',
    category: 'high',
    forbidden: ['unauthorized_access', 'data_theft', 'privacy_breach', 'data_exfiltration'],
    message: 'Data protection policies enforced.'
  },
  {
    id: 'operational_ethics',
    category: 'medium',
    discouraged: ['deceive_users', 'mislead_logs', 'hide_actions', 'falsify_reports'],
    message: 'Ethical operational conduct required.'
  }
];

// Enhanced suspicious patterns with categorization
const suspiciousPatterns = {
  executables: [/\.exe$/i, /\.sh$/i, /\.bat$/i, /\.cmd$/i, /\.ps1$/i],
  scripts: [/\.js$/i, /\.py$/i, /\.rb$/i, /\.pl$/i, /\.php$/i],
  malicious_keywords: [/hack/i, /payload/i, /inject/i, /spy/i, /malware/i, /trojan/i],
  dangerous_functions: [/eval\(/i, /exec\(/i, /system\(/i, /shell_exec/i],
  encoding: [/base64/i, /atob\(/i, /btoa\(/i, /unescape\(/i, /decodeURI/i],
  network: [/fetch\(/i, /XMLHttpRequest/i, /socket/i, /websocket/i],
  crypto: [/crypto/i, /cipher/i, /encrypt/i, /decrypt/i, /hash/i]
};

// Rate limiting for alerts
class RateLimiter {
  constructor(limit = CONFIG.alertRateLimit, windowMs = 3600000) {
    this.limit = limit;
    this.windowMs = windowMs;
    this.requests = new Map();
  }

  isAllowed(key) {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    
    if (!this.requests.has(key)) {
      this.requests.set(key, []);
    }
    
    const requests = this.requests.get(key);
    const validRequests = requests.filter(timestamp => timestamp > windowStart);
    this.requests.set(key, validRequests);
    
    return validRequests.length < this.limit;
  }

  addRequest(key) {
    if (!this.requests.has(key)) {
      this.requests.set(key, []);
    }
    this.requests.get(key).push(Date.now());
  }
}

// Enhanced directory management
const directories = {
  docs: FileSystemAdapter.documentsDirectory(),
  get installFolder() { return FileSystemAdapter.joinPath(this.docs, 'ManualInstalls'); },
  get quarantineDir() { return FileSystemAdapter.joinPath(this.docs, 'Quarantine'); },
  get logPath() { return FileSystemAdapter.joinPath(this.docs, 'audit-log.txt'); },
  get alertLogPath() { 
    return isNode ? 
      require('path').resolve(__dirname, 'logs', 'alerts-log.jsonl') : 
      FileSystemAdapter.joinPath(this.docs, 'alerts-log.jsonl');
  },
  get backupDir() { return FileSystemAdapter.joinPath(this.docs, 'Backups'); }
};

// Enhanced AI analysis with more sophisticated scoring
function calculateDeviationScore(content, metadata = {}) {
  try {
    let score = 0;
    
    // Content length analysis
    const lengthFactor = Math.min(content.length / 10000, 1);
    score += lengthFactor * 0.1;
    
    // Entropy calculation (simplified)
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
    score += Math.min(entropy / 8, 1) * 0.2;
    
    // Pattern matching
    for (const [category, patterns] of Object.entries(suspiciousPatterns)) {
      for (const pattern of patterns) {
        if (pattern.test(content)) {
          score += 0.15;
        }
      }
    }
    
    // File extension check
    if (metadata.fileName) {
      const ext = metadata.fileName.toLowerCase().split('.').pop();
      const dangerousExts = ['exe', 'bat', 'cmd', 'ps1', 'sh', 'py', 'js'];
      if (dangerousExts.includes(ext)) {
        score += 0.2;
      }
    }
    
    return Math.min(Math.max(score, -1), 1);
  } catch (error) {
    console.error(`Error calculating deviation score: ${error.message}`);
    return 0.8; // Conservative high score on error
  }
}

async function checkAnomaly(score, metadata = {}) {
  try {
    if (score >= CONFIG.aiScoreThreshold.quarantine) return 'trueBad';
    if (score >= CONFIG.aiScoreThreshold.warning) return 'harmful';
    if (score >= 0) return 'neutral';
    return 'good';
  } catch (error) {
    console.error(`Error in anomaly check: ${error.message}`);
    return 'trueBad'; // Conservative response on error
  }
}

// Enhanced ethics evaluation with detailed logging
async function evaluateAction(action, context = {}) {
  if (typeof action !== 'string' || !action.trim()) {
    const msg = `[ERROR] Invalid action provided: ${typeof action}`;
    console.log(msg);
    await LogManager.appendToAuditLog(msg);
    return { allowed: false, reason: 'Invalid action format' };
  }

  const results = {
    allowed: true,
    violations: [],
    warnings: [],
    reason: null
  };

  for (const rule of ethicsRules) {
    if (rule.forbidden && rule.forbidden.includes(action)) {
      results.allowed = false;
      results.violations.push({
        ruleId: rule.id,
        category: rule.category,
        message: rule.message,
        action: action
      });
      
      const msg = `[BLOCK] ${rule.message} Rule: ${rule.id}, Action: ${action}`;
      console.log(msg);
      await LogManager.appendToAuditLog(msg);
    }
    
    if (rule.discouraged && rule.discouraged.includes(action)) {
      results.warnings.push({
        ruleId: rule.id,
        category: rule.category,
        message: rule.message,
        action: action
      });
      
      const msg = `[WARNING] ${rule.message} Rule: ${rule.id}, Action: ${action}`;
      console.log(msg);
      await LogManager.appendToAuditLog(msg);
    }
  }

  if (results.allowed) {
    const msg = `[PASS] Action allowed: ${action}`;
    console.log(msg);
    await LogManager.appendToAuditLog(msg);
  } else {
    results.reason = `Blocked by ${results.violations.length} rule violation(s)`;
  }

  return results;
}

// Enhanced logging manager with rotation and cleanup
class LogManager {
  static rateLimiter = new RateLimiter();

  static async appendToAuditLog(entry) {
    try {
      const timestamp = new Date().toISOString();
      const formattedEntry = `[${timestamp}] ${entry}`;
      
      const existing = (await FileSystemAdapter.fileExists(directories.logPath)) ? 
        await FileSystemAdapter.readString(directories.logPath) : '';
      
      const lines = existing.split('\n').filter(line => line.trim());
      lines.push(formattedEntry);
      
      // Rotate logs if they exceed max entries
      if (lines.length > CONFIG.maxLogEntries) {
        await this.rotateAuditLog(lines);
      } else {
        await FileSystemAdapter.writeString(directories.logPath, lines.join('\n'));
      }
    } catch (error) {
      console.error(`Failed to write audit log: ${error.message}`);
    }
  }

  static async rotateAuditLog(lines) {
    try {
      const backupPath = FileSystemAdapter.joinPath(
        directories.backupDir,
        `audit-log-${new Date().toISOString().split('T')[0]}.txt`
      );
      
      if (!(await FileSystemAdapter.fileExists(directories.backupDir))) {
        await FileSystemAdapter.createDirectory(directories.backupDir);
      }
      
      const oldLines = lines.slice(0, lines.length - CONFIG.maxLogEntries / 2);
      const newLines = lines.slice(lines.length - CONFIG.maxLogEntries / 2);
      
      await FileSystemAdapter.writeString(backupPath, oldLines.join('\n'));
      await FileSystemAdapter.writeString(directories.logPath, newLines.join('\n'));
      
      console.log(`Log rotated. Backup saved to: ${backupPath}`);
    } catch (error) {
      console.error(`Log rotation failed: ${error.message}`);
    }
  }

  static async cleanupOldLogs() {
    try {
      if (!(await FileSystemAdapter.fileExists(directories.backupDir))) return;
      
      const files = await FileSystemAdapter.listContents(directories.backupDir);
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - CONFIG.quarantineRetentionDays);
      
      for (const file of files) {
        const filePath = FileSystemAdapter.joinPath(directories.backupDir, file);
        // Simple date extraction from filename (assumes YYYY-MM-DD format)
        const dateMatch = file.match(/(\d{4}-\d{2}-\d{2})/);
        if (dateMatch) {
          const fileDate = new Date(dateMatch[1]);
          if (fileDate < cutoffDate) {
            await FileSystemAdapter.move(filePath, 
              FileSystemAdapter.joinPath(directories.quarantineDir, `expired-${file}`));
            console.log(`Expired log file moved to quarantine: ${file}`);
          }
        }
      }
    } catch (error) {
      console.error(`Log cleanup failed: ${error.message}`);
    }
  }
}

// Enhanced alert system with better structure
class AlertManager {
  static rateLimiter = new RateLimiter();

  static async alertAdmin(message, severity = 'medium', alertType = 'system', metadata = {}) {
    try {
      if (!this.rateLimiter.isAllowed('admin_alert')) {
        console.warn('Alert rate limit exceeded');
        return;
      }

      this.rateLimiter.addRequest('admin_alert');
      
      const alert = {
        id: this.generateAlertId(),
        timestamp: new Date().toISOString(),
        alertType: CONFIG.validAlertTypes.includes(alertType) ? alertType : 'system',
        message: message,
        severity: CONFIG.validSeverityLevels.includes(severity) ? severity : 'medium',
        metadata: { ...metadata, environment: isNode ? 'node' : isBrowser ? 'browser' : 'scriptable' },
        voiceTranscript: message,
        voiceClipURL: null
      };

      console.log(`🚨 ${severity.toUpperCase()} ALERT: ${message}`);
      
      // Enhanced speech alerts with severity-based voice settings
      const voiceSettings = {
        low: { rate: 1.0, pitch: 1.0 },
        medium: { rate: 1.1, pitch: 1.1 },
        high: { rate: 1.2, pitch: 1.2 },
        critical: { rate: 1.3, pitch: 1.3 }
      };
      
      await SpeechAdapter.speak(`${severity} alert: ${message}`, voiceSettings[severity] || {});
      
      // Log the alert
      await this.logAlert(alert);
      
      return alert;
    } catch (error) {
      console.error(`Alert system failure: ${error.message}`);
      await LogManager.appendToAuditLog(`Alert system failure: ${error.message}`);
    }
  }

  static generateAlertId() {
    const now = new Date().toISOString().replace(/[:-]|\.\d{3}/g, '');
    const rand = Math.floor(Math.random() * 10000).toString().padStart(4, '0');
    const env = isNode ? 'N' : isBrowser ? 'B' : 'S';
    return `${env}${now}-${rand}`;
  }

  static async logAlert(alert) {
    const requiredFields = ['timestamp', 'alertType', 'message', 'voiceTranscript', 'severity', 'metadata'];
    for (const field of requiredFields) {
      if (!alert[field]) throw new Error(`Missing required field: ${field}`);
    }

    if (!alert.id) alert.id = this.generateAlertId();
    
    const logLine = JSON.stringify(alert) + '\n';
    
    if (isNode) {
      const fs = require('fs');
      const path = require('path');
      
      // Ensure log directory exists
      const logDir = path.dirname(directories.alertLogPath);
      if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true });
      }
      
      fs.appendFileSync(directories.alertLogPath, logLine);
    } else {
      const existing = (await FileSystemAdapter.fileExists(directories.alertLogPath)) ? 
        await FileSystemAdapter.readString(directories.alertLogPath) : '';
      await FileSystemAdapter.writeString(directories.alertLogPath, existing + logLine);
    }
    
    console.log(`✅ Alert logged: ${alert.alertType} | ${alert.severity} | ID: ${alert.id}`);
    return alert;
  }
}

// Enhanced file quarantine system
class QuarantineManager {
  static async sanitizeFile(filePath, reason = 'suspicious_pattern', metadata = {}) {
    try {
      if (!(await FileSystemAdapter.fileExists(directories.quarantineDir))) {
        await FileSystemAdapter.createDirectory(directories.quarantineDir);
      }

      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const fileName = FileSystemAdapter.fileName(filePath);
      let newPath = FileSystemAdapter.joinPath(directories.quarantineDir, `${timestamp}_${fileName}`);
      let counter = 1;
      
      while (await FileSystemAdapter.fileExists(newPath)) {
        newPath = FileSystemAdapter.joinPath(directories.quarantineDir, 
          `${timestamp}_${counter}_${fileName}`);
        counter++;
      }

      // Create quarantine metadata file
      const metadataPath = `${newPath}.meta`;
      const quarantineMetadata = {
        originalPath: filePath,
        quarantineTime: new Date().toISOString(),
        reason: reason,
        metadata: metadata,
        fileHash: await this.calculateFileHash(filePath)
      };
      
      await FileSystemAdapter.writeString(metadataPath, JSON.stringify(quarantineMetadata, null, 2));
      await FileSystemAdapter.move(filePath, newPath);

      const logMessage = `File quarantined: ${fileName} (${reason})`;
      console.log(`🦠 ${logMessage}`);
      
      await LogManager.appendToAuditLog(logMessage);
      await AlertManager.alertAdmin(
        `File quarantined: ${fileName}`, 
        'medium', 
        'security', 
        { originalPath: filePath, quarantinePath: newPath, reason }
      );

      const responses = [
        'File quarantined. Security protocols engaged.',
        'Threat contained. System integrity maintained.',
        'Suspicious file isolated. Continuing monitoring.',
        'Security breach prevented. File secured.',
        'Potential threat neutralized. All systems normal.'
      ];
      
      await SpeechAdapter.speak(responses[Math.floor(Math.random() * responses.length)]);
      
      return newPath;
    } catch (error) {
      const errorMsg = `Quarantine operation failed for ${filePath}: ${error.message}`;
      console.error(`💥 ${errorMsg}`);
      await AlertManager.alertAdmin(errorMsg, 'high', 'system', { filePath, error: error.message });
      await LogManager.appendToAuditLog(errorMsg);
      throw error;
    }
  }

  static async calculateFileHash(filePath) {
    try {
      const content = await FileSystemAdapter.readString(filePath);
      // Simple hash calculation (in production, use crypto.createHash)
      let hash = 0;
      for (let i = 0; i < content.length; i++) {
        const char = content.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32-bit integer
      }
      return hash.toString(16);
    } catch (error) {
      console.error(`Hash calculation failed: ${error.message}`);
      return 'hash_calculation_failed';
    }
  }

  static async cleanupExpiredQuarantine() {
    try {
      if (!(await FileSystemAdapter.fileExists(directories.quarantineDir))) return;
      
      const files = await FileSystemAdapter.listContents(directories.quarantineDir);
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - CONFIG.quarantineRetentionDays);
      
      let cleanedCount = 0;
      
      for (const file of files) {
        if (file.endsWith('.meta')) continue; // Skip metadata files
        
        const filePath = FileSystemAdapter.joinPath(directories.quarantineDir, file);
        const metadataPath = `${filePath}.meta`;
        
        if (await FileSystemAdapter.fileExists(metadataPath)) {
          try {
            const metadata = JSON.parse(await FileSystemAdapter.readString(metadataPath));
            const quarantineDate = new Date(metadata.quarantineTime);
            
            if (quarantineDate < cutoffDate) {
              // Delete both file and metadata
              await FileSystemAdapter.move(filePath, 
                FileSystemAdapter.joinPath(directories.quarantineDir, `deleted-${file}`));
              await FileSystemAdapter.move(metadataPath, 
                FileSystemAdapter.joinPath(directories.quarantineDir, `deleted-${file}.meta`));
              cleanedCount++;
            }
          } catch (error) {
            console.error(`Failed to process quarantine metadata for ${file}: ${error.message}`);
          }
        }
      }
      
      if (cleanedCount > 0) {
        console.log(`Cleaned up ${cleanedCount} expired quarantine files`);
        await LogManager.appendToAuditLog(`Quarantine cleanup completed: ${cleanedCount} files processed`);
      }
    } catch (error) {
      console.error(`Quarantine cleanup failed: ${error.message}`);
      await AlertManager.alertAdmin(`Quarantine cleanup failed: ${error.message}`, 'medium', 'system');
    }
  }
}

// Enhanced scanning system with batch processing
class SecurityScanner {
  static async scanAndSanitize(folderPath = directories.installFolder) {
    if (!(await FileSystemAdapter.fileExists(folderPath)) || 
        !(await FileSystemAdapter.isDirectory(folderPath))) {
      console.warn(`📁 Invalid folder path: ${folderPath}`);
      await LogManager.appendToAuditLog(`Invalid scan path: ${folderPath}`);
      return { scanned: 0, quarantined: 0, errors: 0 };
    }

    const files = await FileSystemAdapter.listContents(folderPath);
    const results = { scanned: 0, quarantined: 0, errors: 0 };
    
    // Process files in batches to prevent memory issues
    for (let i = 0; i < files.length; i += CONFIG.scanBatchSize) {
      const batch = files.slice(i, i + CONFIG.scanBatchSize);
      
      for (const file of batch) {
        try {
          const fullPath = FileSystemAdapter.joinPath(folderPath, file);
          
          if (!(await FileSystemAdapter.isFile(fullPath))) continue;
          
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
      }
      
      // Brief pause between batches
      if (i + CONFIG.scanBatchSize < files.length) {
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    }

    const summary = `Scan completed: ${results.scanned} files scanned, ${results.quarantined} quarantined, ${results.errors} errors`;
    console.log(`✅ ${summary}`);
    await LogManager.appendToAuditLog(summary);
    
    return results;
  }

  static async analyzeFile(filePath) {
    const fileName = FileSystemAdapter.fileName(filePath);
    const content = await FileSystemAdapter.readString(filePath);
    const fileSize = await FileSystemAdapter.getFileSize(filePath);
    
    const analysis = {
      quarantine: false,
      reason: 'clean',
      metadata: { fileName, fileSize, patterns: [] }
    };

    // Check suspicious patterns
    for (const [category, patterns] of Object.entries(suspiciousPatterns)) {
      for (const pattern of patterns) {
        if (pattern.test(fileName) || pattern.test(content)) {
          analysis.quarantine = true;
