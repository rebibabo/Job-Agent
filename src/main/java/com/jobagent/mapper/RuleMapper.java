package com.jobagent.mapper;

import com.jobagent.dto.RuleFindDTO;
import com.jobagent.dto.RuleSaveDTO;
import com.jobagent.vo.RuleVO;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface RuleMapper {

    void saveRule(@Param("ruleSaveDTO") RuleSaveDTO ruleSaveDTO);

    @Select("select count(*) > 0 from user_rule where user_id=#{ruleFindDTO.userId} and rule_name=#{ruleFindDTO.ruleName}")
    Integer findRule(@Param("ruleFindDTO") RuleFindDTO ruleFindDTO);

    @Select("select * from user_rule where user_id=#{userId}")
    List<RuleVO> loadRule(Integer userId);

    @Delete("delete from user_rule where id=#{ruleId}")
    void deleteRule(Integer ruleId);
}
