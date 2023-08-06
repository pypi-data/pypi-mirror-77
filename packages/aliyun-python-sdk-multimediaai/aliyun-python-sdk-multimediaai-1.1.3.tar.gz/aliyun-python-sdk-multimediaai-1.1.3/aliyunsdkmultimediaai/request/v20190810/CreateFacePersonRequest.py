# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkmultimediaai.endpoint import endpoint_data

class CreateFacePersonRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'multimediaai', '2019-08-10', 'CreateFacePerson')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_FaceGroupId(self):
		return self.get_query_params().get('FaceGroupId')

	def set_FaceGroupId(self,FaceGroupId):
		self.add_query_param('FaceGroupId',FaceGroupId)

	def get_ImageUrls(self):
		return self.get_query_params().get('ImageUrls')

	def set_ImageUrls(self,ImageUrls):
		self.add_query_param('ImageUrls',ImageUrls)

	def get_FacePersonName(self):
		return self.get_query_params().get('FacePersonName')

	def set_FacePersonName(self,FacePersonName):
		self.add_query_param('FacePersonName',FacePersonName)