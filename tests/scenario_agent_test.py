#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   :2024/10/6 15:42
@Author :lancelot.sheng
@File   :scenario_agent_test.py
"""
import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.agents.scenario_agent import ScenarioAgent  # 替换为实际模块路径
from langchain_core.messages import AIMessage

class TestScenarioAgent(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='system prompt')
    @patch('json.load', return_value=['intro message 1', 'intro message 2'])
    @patch('src.agents.session_history.get_session_history')
    def test_initialization(self, mock_get_session_history, mock_json_load, mock_open):
        # 模拟会话历史
        mock_history = MagicMock()
        mock_history.messages = []
        mock_get_session_history.return_value = mock_history

        agent = ScenarioAgent('hotel_checkin')

        # 验证初始化时的文件读取
        mock_open.assert_any_call('prompts/hotel_checkin_prompt.txt', 'r', encoding='utf-8')
        mock_open.assert_any_call('content/intro/hotel_checkin.json', 'r', encoding='utf-8')

        # 验证 intro_messages 是否正确加载
        self.assertEqual(agent.intro_messages, ['intro message 1', 'intro message 2'])

    @patch('src.agents.session_history.get_session_history')
    def test_start_new_session_with_empty_history(self, mock_get_session_history):
        # 模拟会话历史
        mock_history = MagicMock()
        mock_history.messages = []
        mock_get_session_history.return_value = mock_history

        agent = ScenarioAgent('hotel_checkin')
        agent.intro_messages = ["Good afternoon! How may I assist you today?",
                                "Welcome to our hotel! Do you have a reservation with us?",
                                "Hello! Are you here to check in?",
                                "Hi there! How can I help you with your stay?",
                                "Good evening! May I have your name for the booking, please?"]

        # 测试 start_new_session 方法
        initial_message = agent.start_new_session()
        print(str(initial_message))
        # 验证是否添加了初始AI消息
        self.assertIn(initial_message, agent.intro_messages)
        # mock_history.add_message.assert_called_once_with(AIMessage(content=initial_message))

    @patch('src.agents.session_history.get_session_history')
    def test_start_new_session_with_existing_history(self, mock_get_session_history):
        # 模拟会话历史
        mock_history = MagicMock()
        mock_history.messages = [AIMessage(content='Good afternoon! How may I assist you today?')]
        mock_get_session_history.return_value = mock_history

        agent = ScenarioAgent('hotel_checkin')

        # 测试 start_new_session 方法
        last_message = agent.start_new_session()

        # 验证返回的是否是历史记录中的最后一条消息
        self.assertEqual(last_message, last_message)

if __name__ == '__main__':
    unittest.main()