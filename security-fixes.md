# 安全修复指南

**设备**：Khadas (Ubuntu 24.04)
**检查时间**：2026-02-25

---

## 🔴 立即修复（高优先级）

### 1. 禁用 SSH 根登录

**当前状态**：`PermitRootLogin yes`
**风险**：允许直接使用 root 账户登录

**修复步骤**：
```bash
# 1. 备份配置文件
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# 2. 修改配置
sudo sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# 3. 验证修改
grep "PermitRootLogin" /etc/ssh/sshd_config

# 4. 重启 SSH 服务
sudo systemctl restart sshd

# 5. 验证 SSH 仍在运行
sudo systemctl status sshd
```

**验证方法**：
```bash
# 尝试 root 登录（应该失败）
ssh root@localhost
```

**回滚方法**：
```bash
sudo cp /etc/ssh/sshd_config.backup /etc/ssh/sshd_config
sudo systemctl restart sshd
```

---

### 2. 关闭未知端口 5555

**当前状态**：端口 5555 对所有接口开放
**风险**：未知服务对外暴露

**调查步骤**：
```bash
# 查找占用端口的进程
sudo lsof -i :5555
sudo netstat -tlnp | grep 5555
```

**修复步骤**（如确认不需要）：
```bash
# 方法1：使用 UFW 防火墙阻止
sudo ufw deny 5555
sudo ufw reload

# 验证规则
sudo ufw status numbered
```

**如果需要保留此端口**：
```bash
# 限制仅本地访问
sudo ufw allow from 127.0.0.1 to any port 5555
sudo ufw deny from any to any port 5555
```

---

### 3. 限制 SSH 访问来源

**当前状态**：SSH（端口 22）对所有接口开放
**风险**：暴露在家庭网络中

**修复步骤**：
```bash
# 允许本地网络访问（假设是 192.168.x.x）
sudo ufw allow from 192.168.0.0/16 to any port 22
sudo ufw allow from 10.0.0.0/8 to any port 22

# 拒绝其他所有来源的 SSH
sudo ufw deny 22

# 重新加载规则
sudo ufw reload

# 验证
sudo ufw status | grep 22
```

**如需从外部访问**：
```bash
# 允许特定 IP（替换为你的公网 IP）
sudo ufw allow from YOUR_IP_ADDRESS to any port 22
```

---

## ⚠️ 中优先级（本周内完成）

### 4. 启用 SSH 密钥认证（推荐）

**当前状态**：可能使用密码登录
**建议**：使用 SSH 密钥更安全

**设置步骤**：
```bash
# 1. 生成 SSH 密钥对（如果还没有）
ssh-keygen -t ed25519 -a 100

# 2. 复制公钥到服务器
ssh-copy-id -i ~/.ssh/id_ed25519.pub khadas@Khadas

# 3. 测试密钥登录
ssh -i ~/.ssh/id_ed25519 khadas@Khadas

# 4. 禁用密码认证（仅密钥登录）
sudo sed -i 's/^#*PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

---

### 5. 配置 OpenClaw 群组策略

**当前状态**：飞书群组策略为 `open`
**风险**：开放群组暴露提升权限的工具

**修复步骤**：
```bash
# 编辑 OpenClaw 配置
nano ~/.openclaw/openclaw.json
```

**修改为**：
```json
{
  "channels": {
    "feishu": {
      "groupPolicy": "allowlist"
    }
  }
}
```

**重启 OpenClaw Gateway**：
```bash
openclaw gateway restart
```

---

### 6. 设置插件白名单

**当前状态**：`plugins.allow` 未设置
**建议**：明确列出信任的插件

**修复步骤**：
```bash
# 编辑配置
nano ~/.openclaw/openclaw.json
```

**添加**：
```json
{
  "plugins": {
    "allow": [
      "feishu"
    ]
  }
}
```

---

## 🔧 低优先级（维护时处理）

### 7. 固定插件版本

**当前状态**：飞书插件版本未固定
**建议**：固定到具体版本号

**修复步骤**：
```bash
# 查看当前版本
npm list @openclaw/feishu

# 固定版本
openclaw plugin install @openclaw/feishu@<具体版本号>
```

---

### 8. 配置自动安全更新

**当前状态**：未检查
**建议**：启用自动安全更新

**检查步骤**：
```bash
# 检查当前状态
apt list --upgradable

# 配置自动安全更新（需要安装 unattended-upgrades）
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## ✅ 验证修复

**运行验证脚本**：
```bash
cd /home/khadas/.openclaw/workspace
./scripts/security-check.sh
```

**检查项目**：
- [ ] SSH 根登录已禁用
- [ ] 端口 5555 已关闭或限制
- [ ] SSH 仅允许特定来源
- [ ] OpenClaw 配置已更新
- [ ] 新配置已生效

---

## 📞 需要帮助？

如果在修复过程中遇到问题：

1. **SSH 无法登录**
   - 使用本地终端直接操作
   - 恢复备份配置：`sudo cp /etc/ssh/sshd_config.backup /etc/ssh/sshd_config`

2. **防火墙规则错误**
   - 查看规则：`sudo ufw status numbered`
   - 删除规则：`sudo ufw delete NUM`

3. **OpenClaw 无法启动**
   - 检查配置：`openclaw status`
   - 查看日志：`journalctl -u openclaw-gateway -n 50`

---

## 📅 修复计划

**今天（立即）**：
- ✅ 禁用 SSH 根登录
- ✅ 关闭端口 5555
- ✅ 限制 SSH 访问

**本周**：
- 配置 SSH 密钥认证
- 调整 OpenClaw 群组策略
- 设置插件白名单

**下次维护**：
- 固定插件版本
- 配置自动安全更新

---

*生成时间：2026-02-25*
*修复状态：待执行*
