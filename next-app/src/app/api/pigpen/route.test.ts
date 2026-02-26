test('GET /api/pigpen returns operators', async () => {
test('GET /api/pigpen returns operators', async () => {
test('GET /api/pigpen returns operators', async () => {
test('GET /api/pigpen returns operators', async () => {
test('GET /api/pigpen returns operators', async () => {
import { test, expect } from '@jest/globals';
import { GET } from './route';

test('GET /api/pigpen returns operators', async () => {
  const response = await GET();
  const data = await response.json();
  expect(Array.isArray(data)).toBe(true);
});
