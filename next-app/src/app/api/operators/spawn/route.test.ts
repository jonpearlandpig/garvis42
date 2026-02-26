test('POST /api/operators/spawn queues task', async () => {
test('POST /api/operators/spawn queues task', async () => {
test('POST /api/operators/spawn queues task', async () => {
test('POST /api/operators/spawn queues task', async () => {
test('POST /api/operators/spawn queues task', async () => {
test('POST /api/operators/spawn queues task', async () => {
import { test, expect } from '@jest/globals';
import { POST } from './route';

const mockRequest = {
  json: async () => ({
    parent_operator_id: 'PP-001',
    task_description: 'Build a simple user profile API',
    max_subagents: 4,
    max_depth: 3,
    current_depth: 0,
  }),
};

test('POST /api/operators/spawn queues task', async () => {
  const response = await POST(mockRequest);
  const data = await response.json();
  expect(data.task_id).toBeDefined();
  expect(data.status).toMatch(/queued|pending_approval/);
});
